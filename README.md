# UnivaliProjApi

API da Confitto utilizando padrão REST, usando FastAPI e PostgreSQL.

# Pré-Requisitos

- Python 3.14+
- uv (gerencia as dependências)
- PostgreSQL ou Docker

# Instalação

## Python

Você vai precisar do [Python](https://www.python.org/downloads/) instalado no sistema e do pip. Normalmente o pip já vem instalado com o Python, mas verifique com `python -m ensurepip --upgrade`.

Para trabalhar com python usando ambiente virtual, use `python -m venv .venv`. Navegar para o ambiente virtual depende do seu sistema operational:

- Windows: `.venv\Scripts\Activate.ps1` (Powershell) ou `.venv\Scripts\activate.bat` (CMD Prompt)
- Linux / macOS: `source .venv/bin/activate`

## UV

UV é o gerenciador de dependências usado. Você pode instalar com `python -m pip install uv`. Use `uv sync` para se certificar que tem as dependências do projeto.

Quando precisar adicionar uma nova dependência ao projeto, use `uv add` em vez do normalmente recomendado `pip install`. Isso garante que a dependência será adicionada ao `uv.lock` e `pyproject.toml`, para que todos tenham as mesmas dependências no projeto.

## PostgreSQL / Docker

Costuma ser preferível usar o Docker, para que todos tenham exatamente o mesmo Postgres instalado. Caso prefira não usar, você pode baixar o [Postgres manualmente](https://www.postgresql.org/download/).

Caso queira usar o Docker, o guia abaixo é para Windows.

Verifique primeiro que você já tem o Windows Subsystem for Linux (WSL). Abra o PowerShell como administrador e digite `wsl --version`.

Caso não tenha, digite `wsl --install`. Isso pode demorar um pouco, e vai exigir reiniciar o computador em algum ponto.

Após instalar o WSL, que normalmente também vai baixar o Ubuntu automaticamente, baixe o [Docker Desktop](https://www.docker.com/products/docker-desktop/?at_exp=DO112.A).

Para configurar o Postgres após abrir o Docker Desktop, primeiro garanta que seu `.env` e/ou `.env.local` possuem as variáveis necessárias:

```
DATABASE_URL="postgresql+psycopg://seu-usuario-aqui:sua-senha-aqui@localhost:5432/confitto-db"
POSTGRES_USER=seu-usuario-aqui
POSTGRES_PASSWORD=sua-senha-aqui
POSTGRES_DB=confitto-db
```

Em seguida, vá ao terminal do VSCode e digite `docker ps` para garantir que o terminal reconhece o comando, e em seguida `docker compose up -d`. O Postgres será configurado de acordo com suas variáveis de ambiente automaticamente.

Não se esqueça de usar `docker compose down` quando não estiver mais desenvolvendo, para que o Docker não fique consumindo CPU e memória desnecessariamente.

# Configurações de ambiente

Use o `.env.example` para criar seu próprio `.env` e `.env.local` conforme necessário. Eles já estão no `.gitignore`, então não serão enviados ao GitHub com commits.

# Alembic

Para as migrações do banco de dados, usamos o Alembic. Certifique-se de usar `alembic upgrade head` para que seu banco esteja na versão mais recente. As migrações estão localizadas em `alembic/versions`.

Caso faça uma entidade do banco, como as que estão em `app/models`, e precise fazer uma migração do banco de dados, use `alembic revision --autogenerate -m "Mensagem em inglês sobre o que a migração faz"`.

# Servidor

Para inicializar o servidor, use `./scripts/dev.sh`. Caso não queira fazer migrações do alembic automaticamente, use `./scripts/dev.sh --no-migrate`. Isso vai inicializar o servidor pelo uvicorn em localhost na porta 8000.

O endereço dos endpoints, por padrão, começa com `/api/v1/`. Para um endpoint `/users`, por exemplo, estaria em `http://localhost:8000/api/v1/users`.

# Ruff

Ruff é um linter que faz correções com base em expressões idiomáticas do Python. Para ver as sugestões dadas, use `ruff check src`. Para implementar as sugestões dadas, use `ruff check src --fix`.