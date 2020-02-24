# Fast Service

## Instructions (Development without docker)

- Set environment:
	```
	$ export APP_SETTINGS="dev"
	$ export FLASK_APP="app:create_app('${APP_SETTINGS}')"
	$ export FLASK_ENV="development"
	$ python manage.py db upgrade
	```

- Run server (Flask):
	```
	$ flask run -h 0.0.0.0 -p 5000 --with-threads
  $ export APP_SETTINGS="[dev, test or prod]"
	$ export FLASK_ENV=$APP_SETTINGS
	$ export DATABASE_URL="postgresql://[db_host]:[db_port]/db_name"
	```

- Run server (Manage):
	```
	$ python manage.py run
	```

- Run test (Unittest):
	```
	$ python manage.py test
	```

- Run test (Coverage):
	```
	$ coverage erase
	$ coverage run manage.py test
	$ coverage report -m
	```

## Instructions (Docker "Development branch")
- Build container:
	```
	$ sudo docker --rm --no-cache --pull fast_service:[version] .
	```

- Run container:
	```
	$ sudo docker run --rm fast_service:[version]
	```

## Instructions (Production)
- Set environment:
	```
	$ export APP_SETTINGS="prod"
	$ export FLASK_APP="app:create_app('${APP_SETTINGS}')"
	$ export FLASK_ENV="production"
	$ export DATABASE_URL="[db_schema]://[db_user]:[db_pass]@[db_host]:[db_port]/[db_name]"
	$ python manage.py db upgrade
	```

- Run server (Gunicorn):
	```
	$ gunicorn -w 4 -b [host]:[port] "$FLASK_APP"
	$ python manage.py run
	```
