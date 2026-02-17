#!/bin/bash
set -e

# Print environment variables for debugging (without password)
echo "==> Starting Odoo with configuration:"
echo "Database Host: ${HOST:-localhost}"
echo "Database Port: ${PORT:-5432}"
echo "Database User: ${USER:-odoo}"
echo "Database Name: ${DB_NAME:-odoo}"

# Wait for PostgreSQL to be ready (with shorter timeout)
echo "==> Checking PostgreSQL connection..."
TIMEOUT=30
COUNTER=0
while ! nc -z ${HOST:-localhost} ${PORT:-5432}; do
  sleep 1
  COUNTER=$((COUNTER+1))
  if [ $COUNTER -ge $TIMEOUT ]; then
    echo "==> Timeout waiting for PostgreSQL. Starting Odoo anyway..."
    break
  fi
  if [ $((COUNTER % 5)) -eq 0 ]; then
    echo "==> Still waiting for PostgreSQL... ($COUNTER seconds)"
  fi
done

if [ $COUNTER -lt $TIMEOUT ]; then
  echo "==> PostgreSQL is ready!"
fi

# Always use --init base to initialize database if needed
echo "==> Starting Odoo server with database initialization..."
exec python /usr/src/odoo/odoo-bin \
  --db_host=${HOST:-localhost} \
  --db_port=${PORT:-5432} \
  --db_user=${USER:-odoo} \
  --db_password=${PASSWORD:-odoo} \
  --database=${DB_NAME:-odoo} \
  --addons-path=/mnt/extra-addons,/usr/src/odoo/addons \
  --http-interface=0.0.0.0 \
  --http-port=8069 \
  --workers=0 \
  --log-level=info \
  --init base
