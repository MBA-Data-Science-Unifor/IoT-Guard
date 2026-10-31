# IoT Guard

Projeto de detecção de intrusão em redes IoT com aprendizado de máquina supervisionado.

## Estrutura

```text
.
├── app.py                         # Aplicação principal Dash
├── dashboard_data.py              # Leitura/cache dos artefatos
├── dashboard_components.py        # Componentes visuais reutilizáveis
├── notebook_reference.py          # Trechos dos notebooks para referência
├── pages/                         # Páginas Dash
├── assets/styles.css              # Identidade visual
├── scripts/build_model_artifacts.py
├── artifacts/notebooks/           # Notebooks metodológicos
└── artifacts/presentation/model/  # Resultados consumidos pelo Dash
```

## Artefatos utilizados

A apresentação lê os arquivos produzidos pelo pipeline analítico:

- `X_train.csv` e `X_test.csv`;
- `y_train.csv` e `y_test.csv`;
- `target_mapping.csv`;
- resultados materializados em `artifacts/presentation/model/`.

Os dados atualmente estão em `artifacts/notebooks/artifacts/model/data/`, e o
carregador também reconhece `artifacts/model/data/` quando esse diretório for
preenchido pelo DVC ou pelos notebooks.

## Execução

Sincronize as dependências:

```bash
uv sync
```

Gere ou atualize os resultados dos três modelos:

```bash
python scripts/build_model_artifacts.py
```

Inicie a apresentação:

```bash
python app.py
```

Acesse <http://127.0.0.1:8050>.

## Páginas da apresentação

- **Visão geral**: contexto, objetivo e dimensão dos artefatos.
- **Dados e preparo**: classes, mapeamento do alvo e explicação do pipeline.
- **Análise exploratória**: distribuições, correlações e estatísticas descritivas.
- **Modelos e métricas**: benchmark, F1-Macro, matrizes e importâncias.
- **Metodologia**: trechos dos notebooks como referência, sem execução dentro do Dash.
- **Conclusão**: interpretação crítica, custos dos erros e próximos passos.

As fórmulas de classificação e F1-Macro são renderizadas em LaTeX pela própria
interface Dash.

## Notebooks

Os notebooks continuam sendo a referência técnica do pipeline:

1. `01_EDA.ipynb`: exploração e codificação inicial.
2. `02_Preprocessing.ipynb`: limpeza, escala, balanceamento e divisão dos dados.
3. `03_Model.ipynb`: otimização e avaliação do LightGBM.

A página de metodologia exibe trechos desses arquivos sem substituir os
artefatos nem executar notebooks durante a navegação.
