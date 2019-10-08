# Fast Service

## Instructions

- Install required packages to run the solution.
	```
	$ pip install -r requirements.txt
	```
- Set environment variables that Flask will use to create a connection to the DB and set the appropiate execution for a production or development environment.
	```
	$ export FLASK_APP="run.py"
    $ export APP_SETTINGS="[development or production]"
	$ export FLASK_ENV=$APP_SETTINGS
	$ export DATABASE_URL="postgresql://[db_host]:[db_port]/db_name"
	```

- Migrate database.
	```
	$ python manage.py db migrate
	$ python manage.py db upgrade
	```

- Run tests.
	```
	$ python manage.py test
	```

- Run server.
	```
	$ python manage.py runserver
	```
