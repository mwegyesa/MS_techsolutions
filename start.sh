#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z ${HOST:-localhost} ${PORT:-5432}; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Start Odoo with environment variables
exec python /usr/src/odoo/odoo-bin \
  --db_host=${HOST:-localhost} \
  --db_port=${PORT:-5432} \
  --db_user=${USER:-odoo} \
  --db_password=${PASSWORD:-odoo} \
  --addons-path=/mnt/extra-addons,/usr/src/odoo/addons \
  --logfile=/var/log/odoo/odoo.log \
  --http-port=8069
