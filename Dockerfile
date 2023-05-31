FROM postgres:latest

ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=medgrabber
COPY ./database/ddl.sql /docker-entrypoint-initdb.d/ddl.sql