# Base instructions
FROM python:3.8.1-slim-buster
RUN apt-get update && apt-get upgrade -y

# Application requirements
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Switch to low-priv user
RUN useradd --create-home waiter
WORKDIR /home/waiter
USER waiter

# Flask environment variables
ENV FLASK_ENV="development"
ENV FLASK_APP="app:create_app('dev')"

# Application deployment
RUN mkdir fast_service
WORKDIR /home/waiter/fast_service
COPY --chown=waiter:waiter . .
RUN python manage.py db upgrade

EXPOSE 5000/tcp
CMD flask run -h 0.0.0.0 -p 5000 --with-threads
