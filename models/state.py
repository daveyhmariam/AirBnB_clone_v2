#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
import os

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship(
        'City', cascade='all ,delete, delete-orphan',
        back_populates='state'
    )

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            from models import storage
            from models.city import City
            res_cities = []
            for value in storage.all(City).values():
                if self.id == value.state_id:
                    res_cities.append(value)
            return res_cities
