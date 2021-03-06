from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app as appl
from models import db

migrate = Migrate(appl, db)
manager = Manager(appl)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()