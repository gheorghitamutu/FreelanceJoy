from flask_restx import Resource

from api.controller.delivered_assets_controller import *
from api.restplus import api
from api.utilities.parsers import delivered_project_asset_input, upload_parser
from api.utilities.serializers import delivered_project_asset_output, message, location, bad_request

projects_assets_namespace = api.namespace('files/projectAssets', description='Operations related to project assets')


@projects_assets_namespace .route('/')
class DeliveredAssetsCollection(Resource):

    @api.response(201, 'ProjectAsset successfully created.', location)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(upload_parser, delivered_project_asset_input)
    def post(self):
        """
        Adds a new project delivered asset
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        args = delivered_project_asset_input.parse_args()
        id = add_delivered_project_asset(uploaded_file, args)

        return {"location": f"{api.base_url}files/projectAssets/{id}"}, 201


@projects_assets_namespace .route('/<int:id>')
@api.response(404, 'ProjectAsset not found.', message)
class DeliveredAsset(Resource):

    @api.marshal_with(delivered_project_asset_output)
    @api.response(200, 'ProjectsAssets successfully queried.')
    def get(self, id):
        """
        Returns a single asset
        """
        return get_delivered_project_asset(id)

    @api.response(200, 'ProjectAsset successfully deleted.', message)
    def delete(self, id):
        """
        Deletes an asset
        """
        delete_delivered_project_asset(id)
        return {'message': f'ProjectAsset with id {id} succesfully deleted '}, 200
