# IoT Guard

Apresentação Streamlit do estudo de detecção de intrusão na base RT-IoT2022. O app lê artefatos já produzidos pelos notebooks; a navegação não executa o pipeline de treino.

## Executar

Requer Python 3.12 ou superior. Na raiz do projeto:

```bash
uv sync --no-dev
uv run --no-dev streamlit run app.py
```

O app tem quatro páginas: Visão Geral, EDA, Pré-processamento e Modelos. A apresentação lê CSVs e monta tabelas com Polars. O Streamlit ainda instala pandas como dependência transitiva, mas o código da apresentação não o importa.

Para executar os notebooks, instale também o grupo de análise: `uv sync --group analysis`. Para atualizar dependências, execute `uv lock` e regenere os arquivos `requirements*.txt` com `uv export`, usando os mesmos grupos indicados no cabeçalho de cada arquivo.

## Pipeline atual

Execute os notebooks em `artifacts/notebooks/` nesta ordem, a partir da raiz do projeto:

1. `01_EDA_merged.ipynb`: carrega 123.117 fluxos, analisa qualidade, distribuição, leakage e relevância; exporta 80 features codificadas e o mapeamento das 12 classes.
2. `02_Preprocessing_merged.ipynb`: faz split estratificado 80/20; ajusta `RobustScaler` apenas no treino; reduz DoS de 75.727 para 10.000 e aplica SMOTE a quatro classes raras até 500. Exporta 34.085 linhas de treino e 24.624 de teste.
3. `03_Model_merged.ipynb`: faz busca com validação cruzada para LightGBM, HistGradientBoosting e RandomForest; avalia o teste completo com F1, Kappa, MCC e Log-Loss, além do recorte de vetores inéditos e curvas de limiar para alerta binário; salva o campeão e os modelos individuais.

O pipeline atual mantém duplicadas e as 80 features. `log1p` e correlação são usados no EDA, mas não são transformações do treino. O notebook 03 só reutiliza o cache do benchmark quando os hashes dos dados e metadados de entrada coincidem.

## Resultado verificado

| Modelo | F1 macro no teste | F1 macro na CV |
|---|---:|---:|
| RandomForest | 0,9557 | 0,9844 |
| HistGradientBoosting | 0,9545 | 0,9822 |
| LightGBM | 0,9508 | 0,9844 |
| Baseline sempre DoS | 0,0724 | — |

O campeão atual é RandomForest. No recorte de 3.576 fluxos cujo vetor não aparece no treino, seu F1 macro é 0,7935. Esse recorte cobre 14,5% do teste e evidencia o efeito das repetições na métrica global. As classes Brute force SSH e Nmap FIN têm apenas 7 e 6 exemplos no teste.

## Artefatos usados

- `artifacts/data/rt_iot2022/RT_IOT2022.csv`: dados brutos.
- `artifacts/model/data/`: dataset codificado, splits, `metadata.json`, `target_mapping.csv` e modelos produzidos pelos notebooks.
- `artifacts/presentation/model/benchmark_models.joblib`: buscas e fingerprint dos arquivos de entrada.
- `artifacts/presentation/model/threshold_metrics.csv` e `limiares_modelos.png`: saídas do notebook de modelagem, não exibidas na apresentação.
- `artifacts/presentation/model/mlops/runs/`: histórico gerado pelo notebook, fora da navegação Streamlit.
- `artifacts/presentation/eda/` e `artifacts/presentation/model/`: gráficos exportados.

Artefatos de benchmark antigos, quando presentes, não alimentam o app atual e não devem ser combinados com as métricas acima.

A Visão Geral apresenta o problema e a equipe. A EDA reúne dicionário de dados, distribuição, estatísticas, valores extremos e limites da base; o Pré-processamento mostra limpeza, codificação, transformações e as 80 features finais; Modelos compara o benchmark, métricas complementares e a queda de F1 nos fluxos inéditos. Os gráficos da página Modelos ficam lado a lado em telas largas e se empilham em telas estreitas.

## Verificação

```bash
uv run --group dev python -m compileall -q app.py pages utils tests
uv run --group dev pytest tests/test_streamlit_pages.py -q -p no:cacheprovider
```

Os testes automatizados verificam a abertura das quatro páginas, a compilação dos notebooks, a consistência dos artefatos e os componentes HTML.
