from . import models

from flask_admin.contrib import sqlamodel
import flask_wtf
import flask_security


class SAUserAdmin(sqlamodel.ModelView):
    def is_accessible(self):
        return flask_security.current_user.has_role('admin')

    def __init__(self, session, endpoint='users_admin', url='users', **kwargs):
        super(SAUserAdmin, self).__init__(
            models.User,
            session, 
            url=url,
            endpoint=endpoint, 
            **kwargs
        )

    list_columns = ['email']

    def get_form(self):
        """ Customize form. """
        form_class = super(SAUserAdmin, self).get_form()
        session = self.session

        class UserForm(form_class):
            role_ids = flask_wtf.SelectMultipleField()
            password = flask_wtf.PasswordField()

            def __init__(self, *args, **kwargs):
                super(UserForm, self).__init__(*args, **kwargs)
                self.role_ids.choices = self.get_role_choices()
                # To delete a field, use this:
                #del self.password

            def get_role_choices(self):
                roles = session.query(models.Role)\
                        .order_by(models.Role.name)
                choices = [(role.id, role.name) for role in roles]
                return choices

        return UserForm

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
