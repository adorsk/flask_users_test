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
    session.commit()
