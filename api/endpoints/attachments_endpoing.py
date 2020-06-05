from flask import request
from flask_restplus import Resource
from api.restplus import api

from api.utilities.serializers import attachment_input, attachment_output, message, location, bad_request
from api.controller.attachments_controller import *

log = logging.getLogger(__name__)

attachments_namespace = api.namespace('files/attachments', description='Operations related to attachments')


@attachments_namespace.route('/')
class AttachmentsCollection(Resource):

    @api.response(201, 'Attachment successfully created.', location)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(attachment_input)
    def post(self):
        """
        Adds a new attachment
        """
        data = request.json
        id = add_attachment(data)
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
