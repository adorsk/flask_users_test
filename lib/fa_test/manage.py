from app import app
import db
from flask_script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


manager = Manager(app)

@manager.command
def recreate_db():
    """ Drop and then created db tables. """
    db.clear_db()
    db.init_db()

if __name__ == '__main__':
    manager.run()
