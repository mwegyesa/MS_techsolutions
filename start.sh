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

# Check if database needs initialization
echo "==> Checking if database needs initialization..."
DB_EXISTS=$(python /usr/src/odoo/odoo-bin --db_host=${HOST:-localhost} --db_port=${PORT:-5432} --db_user=${USER:-odoo} --db_password=${PASSWORD:-odoo} --database=${DB_NAME:-odoo} --list 2>/dev/null | grep -c ${DB_NAME:-odoo} || echo "0")

# Start Odoo with database initialization if needed
echo "==> Starting Odoo server..."

if [ "$DB_EXISTS" = "0" ]; then
  echo "==> Database is empty, will initialize with base module..."
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
else
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
    --log-level=info
fi
