import flask
import flask_security

bp = flask.Blueprint('users', __name__)


@bp.route('/user/<int:user_id>/profile')
@flask_security.login_required
def profile(user_id=None):
    return "profile"
