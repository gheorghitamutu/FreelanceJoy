import logging

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.controller.categories_controller import CategoriesController
import logging
from api.serializers import category_array, category, ids

log = logging.getLogger(__name__)

ns = api.namespace('categories', description='Operations related to project categories')


@ns.route('/', methods=['GET', 'POST'])
class CategoryCollection(Resource):

    @api.response(200, 'Categories successfully queried.')
    @api.marshal_list_with(category)
    def get(self):
        """
        Returns list of  categories.
        """
        categories = CategoriesController.get_categories()

        return categories

    @api.response(201, 'Categories successfully added.')
    @api.expect(category_array)
    def post(self):
        """
        Adds a new list of categories
        """
        data = request.json
        CategoriesController.add_categories(data["categories"])
        message = "resources created"
        return {"message" : message}, 201

    @api.response(204, 'Categories successfully deleted.')
    @api.expect(ids)
    def delete(self):
        """
        Deletes a list of categories
        """
        data = request.json
        CategoriesController.delete_categories(data['ids'])
        return None, 204
