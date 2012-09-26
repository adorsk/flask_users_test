from . import models

from flask_admin.contrib import sqlamodel
import flask_wtf

class SAUserAdmin(sqlamodel.ModelView):
    def __init__(self, session, endpoint='users', **kwargs):
        super(SAUserAdmin, self).__init__(
            models.User,
            session, 
            endpoint=endpoint, 
            **kwargs
        )
    list_columns = ['email']

    def get_form(self):
        """ Customize form. """
        form_class = super(SAUserAdmin, self).get_form()
        # Include validation check for roles.
        setattr(
            form_class, 
            "role_ids", 
            flask_wtf.SelectMultipleField(
                choices=[
                    ('a1', 'Role 1'), 
                    ('a2', 'Role 2')
                ]
            )
        )
        return form_class

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

