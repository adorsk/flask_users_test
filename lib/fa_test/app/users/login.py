from fa_test.app import db
from .models import User, Role
import flask_security

class SAUserDatastore(flask_security.datastore.SQLAlchemyUserDatastore):
    """
    Variation of flask_security.SQLAlchemyUserDatastore, that
    does not require Flask-SQLAlchemy extension.
    """
    def find_user(self, **kwargs):
        return self.db.session.query(self.user_model)\
                .filter_by(**kwargs).first()

    def find_role(self, role):
        return self.db.session.query(self.role_model)\
                .filter_by(id=role).first()

datastore = SAUserDatastore(db, User, Role)
