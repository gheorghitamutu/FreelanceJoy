from flask import request
from flask_restplus import Resource

from api.controller.projects_controller import *
from api.restplus import api
from api.utilities.serializers import project_input, project_output, message, bad_request, location

projects_namespace = api.namespace('projects', description='Operations related to projects')


@projects_namespace.route('/')
@api.response(404, 'Project not found.', message)
class ProjectCollection(Resource):

    @api.response(201, 'Project successfully created.', location)
    @api.response(409, 'Project already exists.', message)
    @api.response(400, 'Bad request.', bad_request)
    @api.expect(project_input)
    def post(self):
        """
        Adds a new project
        """
        data = request.json
        id = add_project(data)
        return {"location": f"{api.base_url}projects/{id}"}, 201


@api.response(404, 'Project not found', message)
@projects_namespace.route('/<int:id>')
class ProjectItem(Resource):

    @api.marshal_with(project_output)
    @api.response(200, 'Projects successfully queried.')
    def get(self, id):
        """
        Return a single project
        """
        return get_project(id)

    @api.response(200, 'Project successfully deleted.', message)
    def delete(self, id):
        """
        Deletes a single project
        """
        delete_project(id)
        return {'message': f'Project with id {id} succesfully deleted '}, 200
