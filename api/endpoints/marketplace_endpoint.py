from flask import request
from flask_restx import Resource

from api.controller.marketplace_controller import *
from api.restplus import api
from api.utilities.parsers import pagination_arguments
from api.utilities.serializers import marketplace_project_input, marketplace_project_output, message, bad_request, \
    page_of_marketplace_projects, location

marketplace_namespace = api.namespace('marketplace', description='Operations related to marketplace projects')


@marketplace_namespace.route('/')
class MarketplaceProjectsCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_marketplace_projects)
    @api.response(200, 'Marketplace Projects successfully queried.')
    def get(self):
        """
        Returns list of marketplace projects
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        category_id = args.get('category_id', None)
        user_email = args.get('user_email', None)
        freelacer_flag = args.get('freelancer_flag', False)

        return get_marketplace_projects(page, per_page, category_id, user_email, freelacer_flag)

    @api.response(201, 'Marketplace Project successfully created.', location)
    @api.response(409, 'Marketplace Project already exists', message)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(marketplace_project_input)
    def post(self):
        """
        Adds a new product
        """
        data = request.json
        id = add_marketplace_project(data)
        return {"location": f"{api.base_url}marketplace/{id}"}, 201


@api.response(404, 'Marketplace Project not found', message)
@marketplace_namespace.route('/<int:id>')
class MarketplaceProjectItem(Resource):

    @api.marshal_with(marketplace_project_output)
    @api.response(200, 'Marketplace Projects successfully queried.')
    def get(self, id):
        """
        Return a single product
        """
        return get_marketplace_project(id)

    @api.response(200, 'Marketplace Project successfully delete.', message)
    def delete(self, id):
        """
        Deletes a single product
        """
        delete_marketplace_project(id)
        return {'message': f'Marketplace Project with id {id} succesfully deleted '}, 200
