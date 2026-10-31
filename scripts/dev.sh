#!/usr/bin/env bash
# Inicia o servidor de desenvolvimento, aplicando as migrações antes por padrão.
#
# Uso: ./scripts/dev.sh [--no-migrate] [argumentos extras do uvicorn]
#   --no-migrate  Pula o `alembic upgrade head`
#
# Variáveis opcionais: HOST (padrão 127.0.0.1) e PORT (padrão 8000).
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

migrate=true
uvicorn_args=()

for arg in "$@"; do
    case "$arg" in
        --no-migrate) migrate=false ;;
        -h|--help)
            sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) uvicorn_args+=("$arg") ;;
    esac
done

# Usa o Python da .venv (Linux/macOS ou Windows) quando existir
if [[ -x .venv/bin/python ]]; then
    python=.venv/bin/python
elif [[ -x .venv/Scripts/python.exe ]]; then
    python=.venv/Scripts/python.exe
else
    python=python
fi

if [[ "$migrate" == true ]]; then
    if [[ ! -f alembic.ini ]]; then
        echo "Erro: alembic.ini não encontrado. Configure o Alembic ou use --no-migrate." >&2
        exit 1
    fi
    echo "==> Aplicando migrações (alembic upgrade head)"
    "$python" -m alembic upgrade head
fi

echo "==> Iniciando o servidor em http://${HOST:-127.0.0.1}:${PORT:-8000}"
exec "$python" -m uvicorn app.main:app \
    --reload \
    --host "${HOST:-127.0.0.1}" \
    --port "${PORT:-8000}" \
    ${uvicorn_args[@]+"${uvicorn_args[@]}"}