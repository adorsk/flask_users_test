from flask import Flask, url_for, render_template
import db


from flask.ext import admin, wtf
from flask.ext.admin.contrib import sqlamodel
from flask.ext.admin.contrib.sqlamodel import filters
import wtforms.widgets as widgets

import users as users
import users.models as users_models
import users.admin as users_admin
import users.data as users_data

import logging

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Configure database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/adorsk/projects/fa_test/db.sqlite'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Simple Models')

    # Setup users.
    users_models.setup_orm(db)
    admin.add_view(users_admin.SAUserAdmin(db.session()))
    #admin.add_view(users_admin.SARoleAdmin(db.session))

    users_data.setup_initial_data(db.session())

    # Create DB
    db.create_all()

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


    # Start app
    app.debug = True
    app.run('0.0.0.0', 8000)
