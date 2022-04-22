#!/bin/bash

set -e
echo "from postgres init"
echo $POSTGRES_USER
echo $DB_USER
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_USER_PASSWORD';
    ALTER DATABASE $POSTGRES_DB OWNER TO $DB_USER;
    \c $POSTGRES_DB
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
EOSQL
