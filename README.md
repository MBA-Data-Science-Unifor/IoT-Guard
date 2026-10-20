# IoT Guard

Apresentação de um projeto de detecção de intrusão em redes IoT com aprendizado de máquina supervisionado.

## Objetivo

O projeto demonstra, de forma visual e objetiva, o problema analisado, a abordagem adotada, os modelos avaliados e os resultados obtidos.

O Streamlit funciona como uma apresentação de slides. Ele exibe textos, trechos selecionados de código, gráficos, métricas e artefatos previamente gerados. Não há treinamento, EDA pesada ou busca do dataset original durante a apresentação.

## Estrutura

```text
.
├── .dockerignore             # Arquivos excluídos do contexto do Docker
├── .gitignore                # Arquivos locais e artefatos ignorados pelo Git
├── Dockerfile                # Imagem da aplicação
├── docker-compose.yml        # Serviços locais da solução
├── dvc.yaml                  # Definição do versionamento de dados e artefatos
├── README.md                 # Documentação e roteiro da apresentação
├── app.py                    # Entrada única do Streamlit
├── presentation/
│   ├── content/              # Textos e narrativa dos slides
│   ├── snippets/             # Trechos de código selecionados para exibição
│   ├── assets/               # Imagens, ícones e elementos visuais
│   └── components/           # Navegação, tema e componentes do Streamlit
├── artifacts/
│   ├── presentation/         # Resultados consumidos pela apresentação
│   │   ├── eda/               # Gráficos e resumos da análise exploratória
│   │   ├── benchmark/         # Comparação entre os modelos avaliados
│   │   ├── metrics/            # Métricas finais de desempenho
│   │   └── figures/            # Figuras, matrizes e visualizações exportadas
│   ├── notebooks/             # Notebooks preservados como documentação técnica
│   └── model/                 # Pipeline, schema, labels e metadados do modelo
├── src/
│   └── iotguard/              # Código técnico de suporte ao projeto
├── services/
│   └── api.py                 # API para testes de inferência
└── tests/                     # Testes automatizados dos componentes técnicos
```

Os notebooks em `artifacts/notebooks/` são materiais de registro e comprovação do processo analítico. Eles não são executados pelo Streamlit; os resultados relevantes são exportados para `artifacts/presentation/`.

## Fluxo da apresentação

1. Contexto e problema;
2. Abordagem do projeto;
3. Dados e características analisadas;
4. Modelos considerados;
5. Resultados e benchmark;
6. Exemplo de inferência;
7. Conclusões e limitações.

A navegação deve permitir tanto o acesso livre pelo menu quanto a passagem sequencial pelos botões de anterior e próximo.

## Artefatos

Os slides consomem arquivos já produzidos, principalmente:

- gráficos e resultados de EDA;
- métricas e comparações de modelos;
- matrizes de confusão e demais figuras;
- schema, labels e metadados do modelo;
- notebooks usados como documentação técnica do processo.

Quando um artefato não estiver disponível, a apresentação deve informar a ausência no slide e continuar funcionando.

Para recuperar artefatos versionados:

```bash
dvc pull
```

## Executar a apresentação

```bash
pip install -r requirements.txt
streamlit run app.py
```

Acesse `http://localhost:8501`.

## Componentes técnicos

O código de treinamento, a API, o simulador, o monitoramento e os testes são componentes de apoio. Eles ficam separados da camada de apresentação e não são executados durante a navegação dos slides.

Para executar a API, quando disponível:

```bash
uvicorn services.api:app --reload --port 8000
```

Para executar os testes:

```bash
pytest -q
```
