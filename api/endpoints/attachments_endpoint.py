from flask_restx import Resource

from api.controller.attachments_controller import *
from api.restplus import api
from api.utilities.parsers import attachment_input, upload_parser
from api.utilities.serializers import attachment_output, message, location, bad_request

log = logging.getLogger(__name__)

attachments_namespace = api.namespace('files/attachments', description='Operations related to attachments')


@attachments_namespace.route('/')
class AttachmentsCollection(Resource):

    @api.response(201, 'Attachment successfully created.', location)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(upload_parser, attachment_input)
    def post(self):
        """
        Adds a new attachment
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        args = attachment_input.parse_args()
        id = add_attachment(uploaded_file, args)
        
        return {"location": f"{api.base_url}files/attachments/{id}"}, 201


@attachments_namespace.route('/<int:id>')
@api.response(404, 'Attachment not found.', message)
class Attachment(Resource):

    @api.marshal_with(attachment_output)
    @api.response(200, 'Attachments successfully queried.')
    def get(self, id):
        """
        Returns a single attachment
        """
        return get_attachment(id)

    @api.response(200, 'Attachment successfully deleted.', message)
    def delete(self, id):
        """
        Deletes an attachment
        """
        delete_attachment(id)
        return {'message': f'Attachment with id {id} succesfully deleted '}, 200
