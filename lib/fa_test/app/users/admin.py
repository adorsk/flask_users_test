from . import models

import flask
from flask import (request, redirect, url_for)
import flask_admin
import flask_admin.base
from flask_admin.contrib import sqlamodel
import flask_wtf
from flask_security import current_user
from flask_security.utils import encrypt_password
import flask_security.decorators as fs_decorators


class SAUserAdmin(sqlamodel.ModelView):

    list_columns = ['email']

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, endpoint='users_admin', url='users', **kwargs):
        super(SAUserAdmin, self).__init__(
            models.User,
            session, 
            url=url,
            endpoint=endpoint, 
            **kwargs
        )

    def get_form(self):
        """ Customize form. """
        form_class = super(SAUserAdmin, self).get_form()
        session = self.session

        class UserBaseForm(form_class):
            role_ids = flask_wtf.SelectMultipleField()
            password = flask_wtf.PasswordField()

            def __init__(self, *args, **kwargs):
                super(UserBaseForm, self).__init__(*args, **kwargs)
                self.role_ids.choices = self.get_role_choices()
                # To delete a field, use this:
                #del self.password

            def get_role_choices(self):
                roles = session.query(models.Role)\
                        .order_by(models.Role.name)
                choices = [(role.id, role.name) for role in roles]
                return choices

        return UserBaseForm

    def edit_form(self, form, obj=None):
        """ Modify user editing form for admins and normal logged in users. """
        base_class = super(self.__class__, self).get_edit_form()

        # Form for admins.
        if current_user.has_role('admin'):
            class AdminEditUserForm(base_class):
                def __init__(self, *args, **kwargs):
                    super(self.__class__, self).__init__(*args, **kwargs)
            form_class = AdminEditUserForm

        # Form for normal users.
        else:
            class NonAdminEditUserForm(base_class):
                def __init__(self, *args, **kwargs):
                    super(self.__class__, self).__init__(*args, **kwargs)
                    del self.role_ids
            form_class = NonAdminEditUserForm

        return form_class(form, obj)

    @flask_admin.base.expose('/edit/')
    def edit_view(self, *args, **kwargs):
        """
            Edit model view
        """

        editing_allowed = True

        # Anonymous users can't edit.
        if not current_user.is_authenticated():
            editing_allowed = False
            return fs_decorators._get_unauthorized_view()

        # Non-admin users can only edit themselves.
        elif not current_user.has_role('admin'):
            if not current_user.id == request.args.get('id'):
                editing_allowed = False
                
        if not editing_allowed:
            return fs_decorators._get_unauthorized_view()

        return super(SAUserAdmin, self).edit_view()

    def on_model_change(self, form, model):
        """ Encrypt password fields. """
        if form.data.get('password'):
            model.password = encrypt_password(form.data['password'])


class SARoleAdmin(sqlamodel.ModelView):
    def __init__(self, session, endpoint='roles', **kwargs):
        super(SARoleAdmin, self).__init__(
            models.Role,
            session, 
            endpoint=endpoint, 
            **kwargs
        )
    list_columns = ['id', 'name']
    form_columns=['id', 'name']
