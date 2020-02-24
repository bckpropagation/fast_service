import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # FLASK CONF
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False

    # SWAGGER CONF
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ["GET"]
    SWAGGER_UI_DOC_EXPANSION = "list"

    # RESTPLUS CONF
    RESTPLUS_MASK_SWAGGER = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "testing"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_by_name = {
        'dev': DevelopmentConfig,
        'test': TestingConfig,
        'prod': ProductionConfig
}

key = str(Config.SECRET_KEY)
