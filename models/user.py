#!/usr/bin/python3
""" holds class User"""
import hashlib
from os import getenv

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


def hash_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    hashed_pwd = md5_hash.hexdigest()
    return hashed_pwd


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            kwargs['password'] = hash_password(kwargs['password'])
        super().__init__(*args, **kwargs)
