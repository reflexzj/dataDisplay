# -*- coding: utf-8 -*-
"""User upload_template."""
import datetime as dt

from flask_login import UserMixin

from dataDisplay.database import Column, Model, SurrogatePK, db, reference_col, relationship
from dataDisplay.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    # name = Column(db.String(80), nullable=False)
    permissions = Column(db.Integer)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, permissions, **kwargs):
        """Create instance."""
        # db.Model.__init__(self, name=name, **kwargs)
        db.Model.__init__(self, permissions=permissions, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    # email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    department = Column(db.String(30), nullable=True)
    town = Column(db.String(30), nullable=True)
    name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)

    def __init__(self, username, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def check_permission(self, permissions):
        if len(self.roles) > 0:
            return self.roles is not None and (self.roles[0].permissions & permissions) == permissions
        else:
            return False

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
