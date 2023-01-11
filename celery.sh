#!/bin/bash

while python manage.py showmigrations | grep '\[ \]'  &> /dev/null; do
echo "Waiting for all migrations to be completed, please wait ..."
sleep 3
done

exec "$@"