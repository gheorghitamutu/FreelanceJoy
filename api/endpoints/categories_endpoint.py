
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.controller.categories_controller import *
import logging
from api.serializers import category_input, category_output

log = logging.getLogger(__name__)

categories_namespace = api.namespace('categories', description='Operations related to project categories')


@categories_namespace.route('/')
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
    @api.response(409, 'Category already exists')
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


@categories_namespace.route('/<int:id>')
@api.response(404, 'Category not found.')
class CategoryItem(Resource):

    @api.marshal_with(category_output)
    @api.response(200, 'Categories successfully queried.')
    def get(self, id):
        """
        Returns a single category
        """
        return get_category(id)

    @api.response(200, 'Category successfully updated')
    @api.response(400, 'Bad request')
    def patch(self, id):
        """
        Updates a category.

        """
        data = request.json
        update_category(id, data)
        return {'message': f'Category with with id {id} succesfully updated'}, 200

    @api.response(200, 'Category successfully deleted.')
    @api.response(404, 'Category not found')
    def delete(self, id):
        """
        Deletes a category.
        """
        delete_category(id)
        return {'message': f'Category with with id {id} succesfully deleted '}, 200
