psql "sslmode=require host=${PGHOST} port=5432 user=oktadmin dbname=oktank" <  oktank_pgdata.sql > dump.log 2>&1
