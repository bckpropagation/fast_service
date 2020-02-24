import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.main import db

# Models
from app.main.model import restaurant
from app.main.model import menu
from app.main.model import user


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(
        host="0.0.0.0",
        port=5000
    )

@manager.command
def test():
    """ Run unit tests """
    tests = unittest.TestLoader().discover('app/test', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0

    return 1


if __name__ == '__main__':
    manager.run()
