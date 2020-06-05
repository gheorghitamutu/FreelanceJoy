from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.controller.jobs_controller import *
import logging
from api.serializers import job_input, job_output, job_output_complete, message, bad_request, page_of_jobs
from api.parsers import pagination_arguments

log = logging.getLogger(__name__)

jobs_namespace = api.namespace('jobs', description='Operations related to jobs')


@jobs_namespace.route('/')
@api.response(404, 'Job not found.', message)
class JobCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_jobs)
    @api.response(200, 'Jobs successfully queried.')
    def get(self):
        """
        Returns list of jobs
        """

        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        jobs_page = get_jobs(page, per_page)
        return jobs_page

    @api.response(201, 'Job successfully created.')
    @api.response(409, 'Job already exists', message)
    @api.response(400, 'Bad request', bad_request)
    @api.expect(job_input)
    def post(self):
        """
        Adds a new job
        """
        data = request.json
        id = add_job(data)
        return {"location": f"{api.base_url}jobs/{id}"}, 201


@api.response(404, 'Job not found', message)
@jobs_namespace.route('/<int:id>')
class JobItem(Resource):

    @api.marshal_with(job_output_complete)
    @api.response(200, 'Jobs successfully queried.')
    def get(self, id):
        """
        Return a single job
        """
        return get_job(id)

    @api.response(200, 'Job successfully delete.', message)
    def delete(self, id):
        """
        Deletes a single job
        """
        delete_job(id)
        return {'message': f'Job with id {id} succesfully deleted '}, 200
