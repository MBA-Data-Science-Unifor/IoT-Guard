# IoT Guard

Projeto de detecção de intrusão em redes IoT com aprendizado de máquina supervisionado.

## Estrutura

```text
.
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── dvc.yaml
├── LICENSE
├── README.md
├── pyproject.toml                 # Dependências e configuração do projeto
├── artifacts/
│   ├── model/                     # Dados processados, pipelines e metadados
│   │   └── data/                  # Matrizes de treino e teste
│   ├── notebooks/                 # Documentação técnica do processo analítico
│   │   ├── 01_EDA.ipynb
│   │   ├── 02_Preprocessing.ipynb
│   │   └── 03_Model.ipynb
│   └── presentation/              # Resultados exportados pelos notebooks
│       ├── eda/                   # Gráficos e tabelas da análise exploratória
│       └── model/                 # Benchmark, métricas e figuras dos modelos
└── uv.lock
```

A estrutura contém somente o pipeline analítico e seus artefatos. Não há, nesta versão, aplicação Streamlit, API, pacote em `src/` ou testes automatizados.

## Fluxo dos notebooks

Execute os notebooks na ordem abaixo:

1. `01_EDA.ipynb`: carrega o RT-IoT2022 e exporta os resultados de EDA para `artifacts/presentation/eda/`.
2. `02_Preprocessing.ipynb`: limpa os dados, faz a divisão estratificada treino/teste e grava os dados processados e metadados em `artifacts/model/`.
3. `03_Model.ipynb`: consome `artifacts/model/data/train.csv` e `test.csv`, treina e compara XGBoost, Random Forest e LightGBM, e grava os resultados em `artifacts/presentation/model/`.

Os dados de treino e teste são gerados exclusivamente pelo `02_Preprocessing.ipynb`:

```text
artifacts/model/data/train.csv
artifacts/model/data/test.csv
```

Os notebooks localizam a raiz do projeto pelo `pyproject.toml` ou `.git`, portanto podem ser executados a partir da raiz ou da pasta `artifacts/notebooks/` sem criar caminhos duplicados como `artifacts/artifacts/`.

## Execução

```bash
uv sync
jupyter notebook artifacts/notebooks/01_EDA.ipynb
```

Depois, execute `02_Preprocessing.ipynb` e `03_Model.ipynb`. O dataset é obtido pelo pacote `ucimlrepo` durante a execução.

Para recuperar artefatos versionados:

```bash
dvc pull
```
