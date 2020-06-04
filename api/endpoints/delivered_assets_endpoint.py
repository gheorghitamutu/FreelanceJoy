from flask import request
from flask_restplus import Resource
from api.restplus import api

from api.serializers import delivered_project_asset_input, delivered_project_asset_output, message, location, bad_request
from api.controller.delivered_assets_controller import *


projects_assets_namespace = api.namespace('files/projectAssets', description='Operations related to project assets')


@projects_assets_namespace .route('/')
class ProjectsAssetsCollection(Resource):

    @api.response(201, 'ProjectAsset successfully created.', location)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(delivered_project_asset_input)
    def post(self):
        """
        Adds a new attachment
        """
        data = request.json
        id = add_delivered_project_asset(data)
        return {"location": f"{api.base_url}files/projectAssets/{id}"}, 201


@projects_assets_namespace .route('/<int:id>')
@api.response(404, 'ProjectAsset not found.', message)
class ProjectAsset(Resource):

    @api.marshal_with(delivered_project_asset_output)
    @api.response(200, 'ProjectsAssets successfully queried.')
    def get(self, id):
        """
        Returns a single attachment
        """
        return get_delivered_project_asset(id)

    @api.response(200, 'ProjectAsset successfully deleted.', message)
    def delete(self, id):
        """
        Deletes an attachment
        """
        delete_delivered_project_asset(id)
        return {'message': f'ProjectAsset with id {id} succesfully deleted '}, 200
