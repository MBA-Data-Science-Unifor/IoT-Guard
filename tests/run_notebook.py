"""Execute notebook cells in the current Python environment and refresh outputs."""
import base64
import contextlib
import io
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

path = Path(sys.argv[1])
notebook = json.loads(path.read_text(encoding="utf-8"))
outputs = []


def display(value):
    data = {"text/plain": repr(value)}
    if hasattr(value, "to_html"):
        data["text/html"] = value.to_html()
    outputs.append({"output_type": "display_data", "data": data, "metadata": {}})


def show(*args, **kwargs):
    for number in plt.get_fignums():
        figure = plt.figure(number)
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", bbox_inches="tight")
        outputs.append({"output_type": "display_data", "data": {
            "image/png": base64.b64encode(buffer.getvalue()).decode("ascii")
        }, "metadata": {}})
    plt.close("all")


plt.show = show
scope = {"__name__": "__main__", "display": display}
execution = 0
for index, cell in enumerate(notebook["cells"]):
    if cell["cell_type"] != "code":
        continue
    print(f"RUN {path.name} cell {index}", flush=True)
    execution += 1
    outputs = []
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(compile("".join(cell["source"]), f"{path.name}:cell:{index}", "exec"), scope)
    if stream.getvalue():
        outputs.insert(0, {"output_type": "stream", "name": "stdout", "text": stream.getvalue().splitlines(keepends=True)})
        print(stream.getvalue()[:2500], flush=True)
    cell["execution_count"] = execution
    cell["outputs"] = outputs
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"OK {path.name}", flush=True)
