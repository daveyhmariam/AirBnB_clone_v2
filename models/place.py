#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity
from models.review import Review


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    user = relationship('User', back_populates='places')
    cities = relationship('City', back_populates='places')
    reviews = relationship(
            'Review',
            cascade='all, delete, delete-orphan',
            back_populates='place'
        )
    amenities = relationship(
        'Amenity', secondary='place_amenity',
        back_populates='place_amenities',
        viewonly=False
    )

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            from models import storage
            result = []
            objs = storage.all(Review)
            for value in objs.values():
                if value.place_id == self.id:
                    result.append(value)
            return result

        @property
        def amenities(self):
            from models import storage

            result = []
            objs = storage.all(Amenity)
            for obj in objs.values():
                for id in self.amenity_ids:
                    if obj.id == id:
                        result.append(obj)
            # for value in storage.all(Amenity).values():
            #    if value.id in self.amenity_ids:
            #       result.append(obj)
            return result

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                    self.amenity_ids.append(value['id'])
