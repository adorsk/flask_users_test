from fa_test.app import app, db
from fa_test.app.users import script as users_script
from flask_script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


manager = Manager(app)

manager.add_command("users", users_script.manager)

@manager.command
def recreate_db():
    """ Drop and then created db tables. """
    db.clear_db()
    db.init_db()

if __name__ == '__main__':
    manager.run()
