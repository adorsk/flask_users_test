from . import models
from flask_security.utils import encrypt_password


def setup_initial_data(session):
    admin_role = models.Role(
        id='admin', 
        name='Admin', 
        description='Administrative role.'
    )
    session.add(admin_role)

    user_defs = [
        {
            'email': 'admin',
            'password': 'admin',
            'active': True,
            'roles': [admin_role]
        },
        {
            'email': 'normal',
            'password':'normal',
            'active': True,
        }
    ]

    for user_def in user_defs:
        user_def['password'] = encrypt_password(user_def['password'])
        user = models.User(**user_def)
        session.add(user)

    session.commit()

