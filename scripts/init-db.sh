#!/bin/bash

set -e
set -u

function create_test_database() {
	psql postgresql://$POSTGRES__USER:$POSTGRES__PASSWORD@$POSTGRES__HOST:$POSTGRES__PORT/$POSTGRES__DATABASE_NAME <<-EOSQL
	    SELECT 'CREATE DATABASE test_$POSTGRES__DATABASE_NAME'
      WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_$POSTGRES__DATABASE_NAME')\gexec
EOSQL
}

create_test_database
echo "postgresql://$POSTGRES__USER:$POSTGRES__PASSWORD@$POSTGRES__HOST:$POSTGRES__PORT/$POSTGRES__DATABASE_NAME"
echo "---- Test database was created ----"