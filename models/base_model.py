#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            from os import getenv
            if getenv('HBNB_TYPE_STORAGE') != 'db':
                for k in ['updated_at', 'created_at']:
                    if k in kwargs.keys():
                        kwargs[k] = datetime.fromisoformat(kwargs[k])
                if '__class__' in kwargs.keys():
                    del kwargs['__class__']

            if 'created_at' not in kwargs.keys():
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()

            for key,  value in kwargs.items():
                setattr(self, key, value)
        models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        self.to_dict()
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        from os import getenv
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            dictionary.update(
                {'__class__': (str(type(self)).split('.')[-1]).split('\'')[0]}
            )

        if "_sa_instance_state" in self.__dict__.keys():
            del self.__dict__["_sa_instance_state"]
        dictionary.update(self.__dict__)
        dictionary['created_at'] = self.__dict__['created_at'].isoformat()
        dictionary['updated_at'] = self.__dict__['updated_at'].isoformat()
        return dictionary

    def delete(self):
        '''delete object by calling the storage delete method'''
        from models import storage
        storage.delete(self)
