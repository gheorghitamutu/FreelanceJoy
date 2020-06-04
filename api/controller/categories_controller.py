import logging

from api.database.models import Category, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from sqlalchemy.orm.exc import NoResultFound


def check_existence(category_id):
    try:
        return Category.query.filter(Category.id == category_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Category with id {category_id} doesn't exist") from e


def get_category(category_id):
    return check_existence(category_id)


def get_categories():
    result = Category.query.all()
    return result


def add_category(category_obj):
    try:
        category = Category(category_obj['name'])
        db.session.add(category)
        db.session.commit()
        return category.id
    except IntegrityError as e:
        raise IntegrityError(f"Category with name {category_obj['name']} already exists", None, None) from e


def delete_category(category_id):
    existent_category = check_existence(category_id)
    db.session.delete(existent_category)
    db.session.commit()


def delete_all_categories():
    categories = get_categories()
    for category in categories:
        db.session.delete(category)
        db.session.commit()


def update_category(category_id, category_obj):
    category = check_existence(category_id)
    for key in category_obj:
        if hasattr(category, key):
            setattr(category, key, category_obj[key])
        else:
            raise AttributeError(f"Input obj has no attribute '{key}'")
    db.session.add(category)
    db.session.commit()
