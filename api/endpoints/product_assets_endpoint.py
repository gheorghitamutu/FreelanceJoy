from flask_restx import Resource

from api.controller.products_assets_controller import *
from api.restplus import api
from api.utilities.parsers import upload_parser, asset_input
from api.utilities.serializers import product_asset_output, message, location, bad_request

assets_namespace = api.namespace('files/productAssets',
                                 description='Operations related to assets belonging to products from marketplace')


@assets_namespace .route('/')
class AssetsCollection(Resource):

    @api.response(201, 'Asset successfully created.', location)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(upload_parser, asset_input)
    def post(self):
        """
        Adds a new image
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        args = asset_input.parse_args()
        id = add_asset(args, uploaded_file)

        return {"location": f"{api.base_url}files/productAssets'/{id}"}, 201


@assets_namespace .route('/<int:id>')
@api.response(404, 'Asset not found.', message)
class Asset(Resource):

    @api.marshal_with(product_asset_output)
    @api.response(200, 'Assets successfully queried.')
    def get(self, id):
        """
        Returns a single image
        """
        return get_asset(id)

    @api.response(200, 'Asset successfully deleted.', message)
    def delete(self, id):
        """
        Deletes an image
        """
        delete_asset(id)
        return {'message': f'Asset with id {id} succesfully deleted.'}, 200
