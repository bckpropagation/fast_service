#!/bin/bash

function create_test_db
{
	echo "CREATE DATABASE test_db;" > init.sql
	echo "GRANt ALL PRIVILEGES ON DATABASE test_db TO $1;" >> init.sql
}

function create_docker_database
{
	echo "ENV DBHOST=localhost" > Dockerfile-database
	echo "ENV POSTGRES_USER=$1" >> Dockerfile-database
	echo "ENV POSTGRES_PASSWORD=$2" >> Dockerfile-database
	echo "ENV POSTGRES_DB=$3" >> database.env

	create_test_db $postgres_user
	echo "ADD init.sql /docker-entrypoint-initdb.d/" >> Dockerfile-database
}

function create_python_dockerfile
{
	echo "[*] Creating Dockerfile-webapp."
	echo "FROM python:rc-alpine" > Dockerfile-webapp
	echo "WORKDIR /app" >> Dockerfile-webapp
	echo "COPY . /app" >> Dockerfile-webapp

	echo -n "[*] Main app file: "
	read app
	echo "ENV FLASK_APP=$app" >> Dockerfile-webapp

	echo -n "[*] Environment: "
	read environment
	echo "ENV APP_SETTINGS=$environment" >> Dockerfile-webapp
	echo "ENV FLASK_ENV=$environment" >> Dockerfile-webapp

	echo "RUN apk add --no-cache postgresql-libs" >> Dockerfile-webapp
	echo "RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev" >> Dockerfile-webapp
	echo "RUN python3 -m pip install -r requirements.txt --no-cache-dir" >> Dockerfile-webapp
	echo "RUN apk --purge del .build-deps" >> Dockerfile-webapp

	echo -n "[*] Postgresql user: "
	read postgres_user

	echo -n "[*] Postgresql password: "
	read postgres_password

	echo -n "[*] Postgresql database name: "
	read postgres_db

	echo "ENV DATABASE_URL='postgresql://$postgres_user:$postgres_password@localhost:5432/$postgres_db'" >> Dockerfile-webapp

	create_docker_database $postgres_user $postgres_password $postgres_db
}

function create_docker_compose
{
	echo "version: \"3.7\"" >> docker-compose.yml
	echo "services: " >> docker-compose.yml
	echo "  web:" >> docker-compose.yml
	echo "    build: " >> docker-compose.yml
	echo "      context: ." >> docker-compose.yml
	echo "      dockerfile: Dockerfile-webapp" >> docker-compose.yml
	echo "      network: host" >> docker-compose.yml
	echo "    ports:" >> docker-compose.yml
	echo "      - 5000:5000" >> docker-compose.yml
	echo "    depends_on:" >> docker-compose.yml
	echo "      - database" >> docker-compose.yml
	echo "  database:" >> docker-compose.yml
	echo "    build:" >> docker-compose.yml
	echo "      context: ." >> docker-compose.yml
	echo "      dockerfile: Dockerfile-database" >> docker-compose.yml
	echo "    restart: always" >> docker-compose.yml
	echo "    volumes: " >> docker-compose.yml
	echo "      - /var/lib/postgres/data" >> docker-compose.yml

}

function is_allowed_to_run_docker
{
	docker_id=$(getent group docker | cut -d : -f 3)

	if [[ -z $(id -G | grep $docker_id) ]]; then
		if [[ $(id -u) != 0 ]]; then
			echo "[*] Not allowed to run docker."
			exit;
		else
			return 0;
		fi
	fi
}


function build
{
	create_python_dockerfile

	is_allowed_to_run_docker
	
	create_docker_compose

	docker-compose --file docker-compose.yml up
	rm init.sql
}

build
