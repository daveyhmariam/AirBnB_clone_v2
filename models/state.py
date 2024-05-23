#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship(
        'City', cascade='all ,delete, delete-orphan',
        backref='state'
    )

    @property
    def cities(self):
        all = models.storage.all()
        cities = []
        result = []
        for key in all:
            if key.split(".")[0] == "City":
                cities.append(all[key])
        for elem in cities:
            if elem.state_id == self.id:
                result.append(elem)
        return result
