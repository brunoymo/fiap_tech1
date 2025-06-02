# API de Vitivinicultura da Embrapa

API pública para consulta dos dados de vitivinicultura disponibilizados pela Embrapa, abrangendo Produção, Processamento, Comercialização, Importação e Exportação.

## Estrutura do Projeto

```
api_vitivinicultura/
├── data/                  # Diretório para armazenamento de dados CSV (mantido na raiz do projeto)
├── README.md              # Este arquivo
├── requirements.txt       # Dependências do projeto
├── run.py                 # Script para iniciar o servidor da API
└── src/                   # Código-fonte do projeto
    ├── api/               # Módulos da API
    │   └── endpoints/     # Endpoints da API por funcionalidade
    ├── main.py            # Ponto de entrada da aplicação FastAPI
    ├── tests/             # Testes automatizados
    └── utils/             # Utilitários (config, csv_downloader, logger, filter_parser)
```

## Funcionalidades

- **Download de CSVs**: Baixa os arquivos CSV diretamente do site da Embrapa.
- **Fallback local**: Usa arquivos CSV locais quando o download falha.
- **Filtragem**: Permite filtrar dados por parâmetros na query string.
- **Documentação automática**: Disponível via Swagger/OpenAPI.

## Endpoints da API

Todos os endpoints seguem o padrão:

- `/api/v1/{modulo}/{tipo}`

Onde:
- `{modulo}` pode ser: `producao`, `processamento`, `comercializacao`, `importacao`, `exportacao`
- `{tipo}` depende do módulo:
  - **producao**: `producao`
  - **processamento**: `viniferas`, `americanas`, `mesa`
  - **comercializacao**: `comercializacao`
  - **importacao**: `vinho`, `espumante`, `frescas`, `passas`, `suco`
  - **exportacao**: `vinho`, `espumante`, `frescas`, `suco`

Exemplo:
- `/api/v1/producao/producao`
- `/api/v1/processamento/viniferas`
- `/api/v1/importacao/vinho`

A resposta de cada endpoint inclui os dados e as subcategorias disponíveis para filtragem.

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Requests
- Pandas
- BeautifulSoup4

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/api-vitivinicultura.git
cd api-vitivinicultura
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

Para iniciar a API:

```bash
python run.py
```

A API estará disponível em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`.

## Funcionamento do Sistema de Download e Fallback

1. **Download**: Ao receber uma requisição, a API tenta baixar o arquivo CSV mais recente do site da Embrapa.
2. **Fallback**: Se o download falhar, usa o arquivo CSV local mais recente.
3. **Filtragem**: Os dados podem ser filtrados via query string.
4. **Subcategorias**: As subcategorias são retornadas junto com os dados.

## Testes

Para executar os testes:

```bash
pytest
```

## Autor

Desenvolvido como parte do Tech Challenge da Pós-Tech em Machine Learning Engineering da FIAP.
