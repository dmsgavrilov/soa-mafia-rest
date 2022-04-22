FROM postgres

WORKDIR /docker-entrypoint-initdb.d
COPY ./schema.sql /docker-entrypoint-initdb.d
COPY ./init-user-db.sh /docker-entrypoint-initdb.d
