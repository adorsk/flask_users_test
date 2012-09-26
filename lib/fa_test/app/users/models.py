from fa_test.app import db
import flask_security
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy


class User(flask_security.UserMixin):
    def __init__(self, id=None, email=None, password=None, roles={}, role_ids=[]):
        self.id = id
        self.email = email
        self.password = password
        if roles:
            self.roles = roles
        elif role_ids:
            self.role_ids = role_ids
        else:
            self.roles = roles

class Role(flask_security.RoleMixin):
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

    def __eq__(self, other):
        return (self.id == other or self.id == getattr(other, 'id', None))

    def __eq__(self, other):
        return (self.id != other or self.id != getattr(other, 'id', None))

    def __str__(self):
        return "%s, %s" % (
            super(Role, self).__str__,
            self.__dict__
        )

class UserRole(object):
    def __init__(self, role=None, user=None, role_id=None):
        if role_id:
            self.role_id = role_id
        else:
            self.role = role
        self.user = user

user_table = Table('user', db.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('email', String),
                   Column('password', String),
                  )

role_table = Table('role', db.metadata,
                   Column('id', String, primary_key=True),
                   Column('name', String),
                   Column('description', Text),
                  )

user_role_table = Table(
    'user__role', db.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', String, ForeignKey('role.id'), primary_key=True),
)

mapper(User, user_table, properties={
    '_user_roles' : relationship(
        UserRole,
        cascade="all, delete-orphan",
    )
})
mapper(Role, role_table)
mapper(UserRole, user_role_table, properties={
    'user': relationship(User),
    'role': relationship(Role),
})

# Proxy UserRole.role_id -> UserRole.role.id .
setattr(
    UserRole, 
    'role_id', 
    association_proxy(
        'role', 
        'id', 
        creator=lambda k: db.session.merge(Role(id=k))
    )
)

# Proxy items in User.roles -> UserRole.role, via _user_roles.
setattr(
    User, 
    'roles', 
    association_proxy('_user_roles', 'role')
)

# Proxy items in User.role_ids -> UserRole.role_id.
setattr(
    User, 
    'role_ids', 
    association_proxy(
        '_user_roles', 
        'role_id', 
        creator=lambda k: UserRole(role_id=k)
    )
)
