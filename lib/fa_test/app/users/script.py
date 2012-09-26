from fa_test.app import db
import flask_script
import data as users_data


manager = flask_script.Manager("User/Role Operations")

@manager.command
def initialize_data():
    """ Populate with initial user/role data. """
    users_data.setup_initial_data(db.session)

