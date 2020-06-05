from api.utilities.files_utility import *
from flask import request
from flask_restplus import Resource
from api.restplus import api
import logging
from api.utilities.serializers import marketplace_file, location, bad_request

log = logging.getLogger(__name__)

marketplace_files_namespace = api.namespace('files/marketplace', description='Operations related to files from marketplace')
storage_manager = GCloudStorage(log, "freelancejoy.appspot.com")

@marketplace_files_namespace.route('/')
class FilesCollection(Resource):

    @api.response(201, 'Attachment successfully created.', location)
    @api.response(400, 'Attachment already exists', bad_request )
    @api.expect(marketplace_file)
    def post(self):
        """
        Adds a new file
        """
        data = request.json
        file_path = f"marketplace/{data['file_name']}"
        link = storage_manager.upload_file(file_path, data['content_as_string'], data['file_type'])
        return {"location": link}, 201
