import logging

from api.database.models import *
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound
log = logging.getLogger(__name__)

def get_category(category_id):
    try:
        return Category.query.filter(Category.id == category_id).one()
    except NoResultFound as e:
        log.exception(e)
        raise NoResultFound(f"Category with id {category_id} doesn't exist") from e



def get_categories():
    result = Category.query.all()
    return result


def add_category(category_obj):
    row = Category(category_obj['name'])
    db.session.add(row)
    db.session.commit()


def delete_category(category_id):
    existent_category = Category.query.filter_by(id=category_id).one()
    if existent_category:
        db.session.delete(existent_category)
        db.session.commit()


def delete_all_categories():
    categories = get_categories()
    for category in categories:
        db.session.delete(category)
        db.session.commit()

def replace_category(category_id, category_obj):
    category = Category.query.filter_by(id=category_id).one()
    category.name = category_obj['name']
    db.session.add(category)
    db.session.commit()


