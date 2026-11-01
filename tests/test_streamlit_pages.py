from pathlib import Path
from unittest.mock import patch
import json
import hashlib

import joblib
import polars as pl

from streamlit.testing.v1 import AppTest

from utils.styles import callout, kpi_grid, page_header
from utils.config import DISTRIBUICAO_TREINO, DISTRIBUICAO_TESTE


def test_callout_renders_markdown_as_valid_html():
    with patch("utils.styles.st.html") as html:
        callout("**Destaque** e `código`\n\n- primeiro\n- segundo\n\n<script>alert(1)</script>")

    rendered = html.call_args.args[0]
    assert "<strong>Destaque</strong>" in rendered
    assert "<code>código</code>" in rendered
    assert "<li>primeiro</li>" in rendered
    assert "**Destaque**" not in rendered
    assert "<script>" not in rendered


def test_html_components_render_as_html_elements():
    with patch("utils.styles.st.html") as html:
        page_header("🛡️", "IoT Guard", "Descrição", "MBA")
        kpi_grid([{"label": "Fluxos", "value": "123.117"}, {"label": "Features", "value": "85"}])

    hero, grid = [call.args[0] for call in html.call_args_list]
    assert '<div class="hero">' in hero
    assert grid.count('<div class="kpi-card') == 2
    assert grid.count('</div>') == 7
    assert "\n" not in grid


def test_all_streamlit_pages_load():
    root = Path(__file__).resolve().parent.parent
    app = AppTest.from_file(root / "app.py").run(timeout=60)
    assert not app.exception, [error.message for error in app.exception]
    for path in sorted((root / "pages").glob("*.py")):
        app.switch_page(f"pages/{path.name}").run(timeout=60)
        assert not app.exception, f"{path.name}: {[error.message for error in app.exception]}"


def test_notebook_cells_compile_and_have_no_recorded_errors():
    root = Path(__file__).resolve().parent.parent
    for path in sorted((root / "artifacts" / "notebooks").glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        ids = [cell.get("id") for cell in notebook["cells"]]
        assert all(ids) and len(ids) == len(set(ids)), path.name
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            compile("".join(cell["source"]), f"{path.name}:cell:{index}", "exec")
            assert not any(output.get("output_type") == "error" for output in cell.get("outputs", []))


def test_preprocessing_artifacts_match_metadata():
    root = Path(__file__).resolve().parent.parent
    model_dir = root / "artifacts" / "model" / "data"
    metadata = json.loads((model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["dos_cap"] == 10000
    assert metadata["n_train_balanced"] == 34085
    assert metadata["n_test"] == 24624
    assert sum(DISTRIBUICAO_TREINO.values()) == metadata["n_train_balanced"]
    assert sum(DISTRIBUICAO_TESTE.values()) == metadata["n_test"]
    for filename, expected in (("X_train.csv", 34085), ("y_train.csv", 34085),
                               ("X_test.csv", 24624), ("y_test.csv", 24624)):
        with (model_dir / filename).open(encoding="utf-8") as handle:
            assert sum(1 for _ in handle) - 1 == expected, filename


def test_benchmark_matches_current_processed_data():
    root = Path(__file__).resolve().parent.parent
    model_dir = root / "artifacts" / "model" / "data"
    benchmark = joblib.load(root / "artifacts" / "presentation" / "model" / "benchmark_models.joblib")
    for name, expected_hash in benchmark["data_fingerprint"].items():
        digest = hashlib.sha256((model_dir / name).read_bytes()).hexdigest()
        assert digest == expected_hash, name


def test_threshold_export_covers_each_model_and_threshold():
    root = Path(__file__).resolve().parent.parent
    data = pl.read_csv(root / "artifacts" / "presentation" / "model" / "threshold_metrics.csv")
    assert set(data["Modelo"]) == {"LightGBM", "HistGradientBoosting", "RandomForest"}
    assert len(data) == 3 * 101
    assert set(data.filter(pl.col("Limiar") == 0.5)["Modelo"]) == set(data["Modelo"])
    for column in ("Precisão", "Recall", "F1", "Especificidade",
                   "Taxa de falsos positivos"):
        assert data[column].is_between(0, 1).all()
