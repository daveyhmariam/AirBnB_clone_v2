#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            obj = dict()
            all_objs = type(self).__objects
            for key in list(all_objs):
                key_split = key.split(".")
                cls_name = key_split[0]
                if cls_name == cls.__name__:
                    obj.update({key:type(self).__objects})
            return obj
        return type(self).__objects

    def delete(self, obj=None):
        '''delete object from __objects'''
        if obj:
            key = type(obj).__name__ + "." + obj.id
            if key in type(self).__objects.keys():
                del type(self).__objects[key]

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({type(obj).__name__ + '.' + obj.id: obj})

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """
        dict = {}

        for key, value in type(self).__objects.items():
            dict[key] = value.to_dict()
        with open(type(self).__file_path, "w") as file:
            json.dump(dict, file, indent=4)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass
    def close(self):
        reload()
        