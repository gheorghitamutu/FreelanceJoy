from  Models import *
from sqlalchemy.exc import SQLAlchemyError
import logging
class CategoriesController:

    @staticmethod
    def get_categories():
        result = Category.query.all()
        schema = CategorySchema(many=True)
        return schema.dump(result)

    @staticmethod
    def add_categories(categories_list):
        try:
            for category in categories_list:
                row = Category(name=category['name'])
                db.session.add(row)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rolleback()
            logging.error(e)
            return False
        return True

    @staticmethod
    def delete_categories(categories_ids_list):
        try:
            for category_id in categories_ids_list:
                existent_category = Category.query.filter_by(id=category_id).first()
                if existent_category:
                    db.session.delete(existent_category)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rolleback()
            logging.error(e)
            return False
        return True


