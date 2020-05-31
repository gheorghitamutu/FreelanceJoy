from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.controller.jobs_controller import *
import logging
from api.serializers import job

log = logging.getLogger(__name__)

jobs_namespace = api.namespace('jobs', description='Operations related to jobs')


@jobs_namespace.route('/')
class JobCollection(Resource):

    @api.marshal_list_with(job)
    @api.response(200, 'Jobs successfully queried.')
    def get(self):
        """
        Returns list of jobs
        """
        jobs = get_jobs()

        return jobs

    @api.response(201, 'Job successfully created.')
    @api.response(409, 'Job already exists')
    @api.expect(job)
    def post(self):
        """
        Adds a new job
        """
        data = request.json
        add_job(data)
        message = "resource created"
        return {"message": message}, 201
