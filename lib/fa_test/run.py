import sys
sys.path.insert(0, '..')


from fa_test.app import app
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
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    if hasattr(flask_config, 'APPLICATION_ROOT'):
        prefix = flask_config.APPLICATION_ROOT
        app.wsgi_app = PrefixFix(app.wsgi_app, '/' + prefix)
        app.config['APPLICATION_ROOT'] = prefix
        app.config['SESSION_COOKIE_PATH'] = '/' + prefix
    app.config['DEBUG'] = True

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    run_simple('localhost', port, app.wsgi_app, use_reloader=True, use_debugger=True)
