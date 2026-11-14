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

Defina `APP_ENV=development` no desenvolvimento. Nesse ambiente, `.env.local`
sobrescreve `.env`; variáveis já exportadas no terminal têm prioridade sobre os
dois arquivos. Em produção e testes, as configurações não carregam esses arquivos.
Defina `APP_ENV=production` explicitamente no Vercel: `VERCEL_ENV` não substitui
`APP_ENV`, e, sem este último, a aplicação assume desenvolvimento.

O Docker Compose lê `.env` por padrão, mas não `.env.local`. Se as credenciais
locais estiverem no segundo arquivo, use
`docker compose --env-file .env --env-file .env.local up -d`.

# Alembic

Para as migrações do banco de dados, usamos o Alembic. Certifique-se de usar `alembic upgrade head` para que seu banco esteja na versão mais recente. As migrações estão localizadas em `alembic/versions`.

Caso faça uma entidade do banco, como as que estão em `app/models`, e precise fazer uma migração do banco de dados, use `alembic revision --autogenerate -m "Mensagem em inglês sobre o que a migração faz"`.

# Servidor

Para inicializar o servidor, use `./scripts/dev.sh`. Caso não queira fazer migrações do alembic automaticamente, use `./scripts/dev.sh --no-migrate`. Isso vai inicializar o servidor pelo uvicorn em localhost na porta 8000.

O endereço dos endpoints, por padrão, começa com `/api/v1/`. Para um endpoint `/users`, por exemplo, estaria em `http://localhost:8000/api/v1/users`.

# Ruff

Ruff é um linter que faz correções com base em expressões idiomáticas do Python. Para ver as sugestões dadas, use `ruff check .` e, para implementar as sugestões dadas, use `ruff check --fix`. O linter já está configurado para olhar apenas o que está dentro da pasta `app/`.

## CORS

Configure `CORS_ORIGINS` no **backend**, com uma lista JSON das origens exatas
dos frontends autorizados. No desenvolvimento, use `.env.local`; no Vercel,
cadastre o valor nas variáveis de ambiente do projeto do backend:

```env
CORS_ORIGINS=["https://seu-projeto.vercel.app"]
```

Para desenvolvimento local, por exemplo:

```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:4200"]
```

Inclua apenas as origens realmente utilizadas. Protocolo, domínio e porta fazem
parte da origem: `http://localhost:3000` difere de `http://127.0.0.1:3000`.
Não inclua caminhos nem barra final. No painel do Vercel, cole a lista JSON
diretamente, sem aspas adicionais envolvendo a lista inteira.

Se houver um domínio próprio, inclua-o também:

```env
CORS_ORIGINS=["https://seu-projeto.vercel.app","https://www.seudominio.com"]
```

A configuração atual em `app/main.py` já permite:

- **Métodos:** todos (`allow_methods=["*"]`), incluindo requisições com `POST`,
  `PUT`, `PATCH` e `DELETE`. O middleware responde automaticamente ao preflight
  `OPTIONS`; não é necessário criar uma rota para ele.
- **Cabeçalhos de requisição:** todos (`allow_headers=["*"]`), incluindo
  `Authorization` e `Content-Type`.
- **Credenciais:** habilitadas (`allow_credentials=True`). Para enviar cookies
  entre origens, o frontend também precisa usar `credentials: "include"` e os
  cookies precisam de atributos apropriados, como `SameSite=None; Secure`
  quando forem entre sites para HTTPS.

Não é necessário configurar variáveis adicionais para métodos ou cabeçalhos.
Essas opções estão no código, não nas variáveis de ambiente. Se quiser
restringi-las, altere o middleware. Cabeçalhos personalizados de **resposta**
que precisem ser lidos pelo JavaScript devem ser listados em `expose_headers`;
nenhum está configurado atualmente.

Use origens explícitas, não `["*"]`, especialmente com credenciais habilitadas.
Sem origens configuradas, o middleware não é instalado e chamadas entre origens
não recebem autorização CORS. CORS não substitui autenticação nem autorização;
permitir um método no middleware não cria endpoints nem libera seu acesso.

Deployments de Preview têm origens próprias. Cadastre explicitamente as origens
necessárias no ambiente correspondente ou use um domínio de preview estável;
não autorize genericamente todos os domínios `*.vercel.app`.

## Backend no Vercel

O Vercel [suporta FastAPI](https://vercel.com/docs/frameworks/backend/fastapi)
e reconhece a instância `app` exportada por `app/main.py`. Configure a raiz deste
repositório como a raiz do projeto do backend e utilize o preset FastAPI.
O runtime suporta Python 3.14, exigido pelo projeto. O script `scripts/dev.sh`
é apenas para desenvolvimento: não o utilize para iniciar o backend no Vercel.

Nas configurações do **projeto do backend**, cadastre:

| Variável | Valor em produção |
| --- | --- |
| `APP_ENV` | `production` |
| `DATABASE_URL` | URL de um PostgreSQL acessível pelo Vercel, com o driver `postgresql+psycopg://` e as opções TLS exigidas pelo provedor |
| `SECRET_KEY` | Segredo longo e aleatório, exclusivo do ambiente |
| `CORS_ORIGINS` | Lista JSON das origens HTTPS do frontend |

`DEBUG` assume `false` em produção; não exporte `DEBUG=true` nesse ambiente.
As rotas `/docs`, `/redoc` e OpenAPI também ficam desabilitadas em produção.
Configure as variáveis separadamente para Production e Preview e faça um novo
deploy após alterá-las. Para Preview, use também `APP_ENV=production` e um banco
isolado, se disponível, evitando executar testes contra o banco de produção.

O Postgres do Docker local não é acessível por `localhost` no Vercel. Use um
provedor de Postgres hospedado e verifique limites de conexão; prefira a URL com
pooling fornecida pelo provedor para funções serverless quando compatível.
As variáveis `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB` do exemplo
inicializam apenas o container local; no backend, a conexão usa `DATABASE_URL`.

Execute `alembic upgrade head` como uma etapa controlada de implantação, com as
variáveis do banco de destino configuradas. Não execute migrações em cada
requisição nem na inicialização de cada instância serverless. Verifique se a
implantação exige uma URL direta, sem pooling, para as migrações.

No frontend, configure a URL pública do backend e faça a requisição para
`https://URL-DO-SEU-BACKEND/test` (não para uma rota relativa do frontend).
Após publicar, valide o preflight usando uma origem cadastrada:

```bash
curl -i -X OPTIONS "https://URL-DO-SEU-BACKEND/test" \
  -H "Origin: https://confitto.vercel.app" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Authorization"
```

A resposta deve conter `Access-Control-Allow-Origin` com a origem enviada e
`Access-Control-Allow-Credentials: true`. Se o Vercel bloquear a requisição
antes de chegar ao FastAPI (por exemplo, pela proteção de deployments de
Preview), ajuste essa proteção para os clientes autorizados; CORS na aplicação
não elimina esse bloqueio.
