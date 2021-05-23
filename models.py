from datetime import datetime

from sqlalchemy import exc

import errors
from app import db


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def to_dict(self):
        response = {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
        return response


class Post(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.today)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def to_dict(self):
        response = {
            "id": self.id,
            "header": self.header,
            "text": self.text,
            "created_date": self.created_date,
            "owner": self.owner_id
        }
        return response


def return_all_posts():
    get = db.session.query(Post).all()
    some_list = []
    for post in get:
        some_list.append({"id": post.id, "header": post.header, "text": post.text,
                          "created_date": str(post.created_date), "owner_id": str(post.owner_id)})
    return some_list
