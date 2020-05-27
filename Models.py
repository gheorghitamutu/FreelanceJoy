from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return '<Test {}>'.format(self.name)


class CategorySchema(ma.Schema):
    class Meta:
        model = Category
        fields = ("id", "name")
        sqla_session = db.session
