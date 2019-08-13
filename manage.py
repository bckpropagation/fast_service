import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from models import dish, review

app = create_app(config_name=os.getenv('APP_SETTINGS'))
app.app_context().push()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """ Run unit tests """
    tests = unittest.TestLoader().discover('./tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0

    return 1


if __name__ == '__main__':
    manager.run()
