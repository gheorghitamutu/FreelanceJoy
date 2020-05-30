
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.controller.categories_controller import *
import logging
from api.serializers import category_input, category_output

log = logging.getLogger(__name__)

ns = api.namespace('categories', description='Operations related to project categories')


@ns.route('/')
class CategoryCollection(Resource):

    @api.marshal_list_with(category_output)
    @api.response(200, 'Categories successfully queried.')
    def get(self):
        """
        Returns list of  categories.
        """
        categories = get_categories()

        return categories

    @api.response(201, 'Category successfully created.')
    @api.response(409, 'Category with id <id> already exists')
    @api.expect(category_input)
    def post(self):
        """
        Adds a new category
        """
        data = request.json
        add_category(data)
        message = "resource created"
        return {"message": message}, 201

    @api.response(204, 'Categories successfully deleted.')
    def delete(self):
        """
        Deletes all categories
        """

        delete_all_categories()
        return None, 204


@ns.route('/<int:id>')
@api.response(404, 'Category not found.')
class CategoryItem(Resource):

    @api.marshal_with(category_output)
    @api.response(200, 'Categories successfully queried.')
    def get(self, id):
        """
        Returns a single category
        """
        return get_category(id)

    @api.response(204, 'Category successfully updated.')
    @api.expect(category_input)
    def put(self, id):
        """
        Updates a category.

        """
        data = request.json
        replace_category(id, data)
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        """
        Deletes a category.
        """
        delete_category(id)
        return None, 204
