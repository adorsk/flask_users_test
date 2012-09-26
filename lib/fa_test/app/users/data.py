from . import models


def setup_initial_data(session):
    setup_initial_roles(session)

def setup_initial_roles(session):
    admin_role = models.Role(
        id='admin', 
        name='Admin', 
        description='Administrative role.'
    )
    session.add(admin_role)

    admin_user = models.User(
        email="admin",
        password="admin",
        active=True,
        roles=[admin_role]
    )
    session.add(admin_user)

    normal_user = models.User(
        email="normal",
        password="normal",
        active=True,
    )
    session.add(normal_user)

    session.commit()

