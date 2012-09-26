import fa_test.flask_config as flask_config
from fa_test.config import config as config
from fa_test.app import db as db

from flask import Flask
import flask_admin


app = Flask(__name__)
app.config.from_object(flask_config)

admin = flask_admin.Admin(app, 'Admin')

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

from fa_test.app.users import models as users_models
from fa_test.app.users import admin as users_admin

admin.add_view(users_admin.SAUserAdmin(db.session))
