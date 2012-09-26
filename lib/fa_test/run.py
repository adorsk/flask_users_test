import sys
sys.path.insert(0, '..')
import getopt

from fa_test import config as fa_config

from werkzeug.serving import run_simple
import flask_config

import logging

class PrefixFix(object):
	def __init__(self, app, script_name):
		self.app = app
		self.script_name = script_name

	def __call__(self, environ, start_response):
		path_info = environ.get('PATH_INFO', '')
		environ['SCRIPT_NAME'] = self.script_name
		if path_info.startswith(self.script_name):
			environ['PATH_INFO'] = path_info[len(self.script_name):]
		return self.app(environ, start_response)

if __name__ == '__main__':
    opts, args = getopt.getopt(
        sys.argv[1:],
        "p: r d:"
    )

    # Defaults.
    port = 8000
    db_url = None
    do_init_db = False

    for opt, value in opts:
        if opt == '-p':
            port = int(value)
        if opt == '-r':
            do_init_db = True
        if opt == '-d':
            db_url = value

    if db_url:
        fa_config.config['DB_URI'] = db_url

    from fa_test.app import app, db

    do_init_db = do_init_db or (str(db.engine.url) == 'sqlite://')
    if do_init_db:
        # have to do it after app starts, due to to
        # threading issues w/ sqlite.
        @app.before_first_request
        def init_db():
            db.clear_db()
            db.init_db()
            from fa_test.app.users import data as users_data
            users_data.setup_initial_data(db.session)

    if hasattr(flask_config, 'APPLICATION_ROOT'):
        prefix = flask_config.APPLICATION_ROOT
        app.wsgi_app = PrefixFix(app.wsgi_app, '/' + prefix)
        app.config['APPLICATION_ROOT'] = prefix
        app.config['SESSION_COOKIE_PATH'] = '/' + prefix
    app.config['DEBUG'] = True

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    run_simple('localhost', port, app.wsgi_app, use_reloader=True, use_debugger=True)
