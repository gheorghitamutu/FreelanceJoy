import logging

from api.database.models import Category
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


def check_existence(category_id):
    try:
        return Category.query.filter(Category.id == category_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Category with id {category_id} doesn't exist") from None


def get_category(category_id):
    return check_existence(category_id)


def get_categories():
    result = Category.query.all()
    return result


def add_category(category_obj):
    try:
        row = Category(category_obj['name'])
        db.session.add(row)
        db.session.commit()
    except IntegrityError as e:
        raise IntegrityError(f"Category with name {category_obj['name']} already exists", None, None) from None


def delete_category(category_id):
    existent_category = check_existence(category_id)
    if existent_category:
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
