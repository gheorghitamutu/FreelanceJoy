import logging

from api.database.models import *
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)


class CategoriesController:
    @staticmethod
    def get_categories():
        result = Category.query.all()
        return result

    @staticmethod
    def add_categories(categories_list):
        for category in categories_list:
            row = Category(category['name'])
            db.session.add(row)
            db.session.commit()


    @staticmethod
    def delete_categories(categories_ids_list):
        for category_id in categories_ids_list:
            existent_category = Category.query.filter_by(id=category_id).first()
            if existent_category:
                db.session.delete(existent_category)
            db.session.commit()

