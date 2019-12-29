
import os


# Uncomment the line below for postgres database url from environment variable
#postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # FLASK CONF
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False

    # SWAGGER CONF
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get"]
    SWAGGER_UI_DOC_EXPANSION = "list"

    # RESTPLUS CONF
    RESTPLUS_MASK_SWAGGER = False


class DevelopmentConfig(Config):
    # Uncomment the line below to use postgres
    #SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTECT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # Uncomment the line below to use postgres
    #SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = {
        'dev': DevelopmentConfig,
        'test': TestingConfig,
        'prod': ProductionConfig
}

key = str(Config.SECRET_KEY)
