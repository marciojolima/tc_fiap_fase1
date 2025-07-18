#!/bin/sh
# Garante que o script pare em caso de erro
set -e

# cd /app

# echo "Entrypoint: Running as root to fix permissions..."
# mkdir -p /app/data || true
# chown -R appuser:appgroup /app/data

# Executa as migrações do banco de dados
echo ">>>> Aplicando migração com alembic <<<<"
alembic upgrade head

# Devolva ao CMD
# exec "$@"
exec "$@"
