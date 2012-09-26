import fa_test.flask_config as flask_config
from fa_test.config import config as config
from fa_test.app import db as db

import flask
import flask_admin
import flask_security


app = flask.Flask(__name__)
app.config.from_object(flask_config)

admin = flask_admin.Admin(app, 'Admin')


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

from fa_test.app.users import models as users_models
from fa_test.app.users import admin as users_admin
from fa_test.app.users import login as users_login
from fa_test.app.users import views as users_views

security = flask_security.Security(app, users_login.datastore)

admin.add_view(users_admin.SAUserAdmin(db.session))

@app.route('/')
def index():
    u = flask_security.current_user
    return "u is: %s" % flask.escape(str(u))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', form=flask_security.LoginForm())

@app.route('/logout')
def logout():
    flask_security.logout_user()
    return redirect(url_for('/'))

app.register_blueprint(users_views.bp, url_prefix='/users')
