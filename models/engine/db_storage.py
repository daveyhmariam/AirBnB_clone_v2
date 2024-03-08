'''database storage for hbnb clone'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    '''database storage class'''

    __engine = None
    __session = None
    _cls = [State, City, User, Place, Review, Amenity]

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')
            ), pool_pre_ping=True
        )
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        result = {}
        key = ''
        if cls is None:
            for cls in self._cls:
                key = cls.__name__ + '.'
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key += obj.id
                    result[key] = obj
        else:
            key = cls.__name__ + '.'
            objs = self.__session.query(cls).all()
            for obj in objs:
                key += obj.id
                result[key] = obj
        return result

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
        return

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Scope_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(Scope_session)
        self.__session = Session()
