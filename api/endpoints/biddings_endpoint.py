from flask import request
from flask_restx import Resource

from api.controller.biddings_controller import *
from api.restplus import api
from api.utilities.serializers import bidding_input, bidding_output, message, bad_request, location

biddings_namespace = api.namespace('biddings', description='Operations related to biddings')


@biddings_namespace.route('/')
@api.response(404, 'Bidding not found.', message)
class BiddingCollection(Resource):

    @api.response(201, 'Bidding successfully created.', location)
    @api.response(409, 'Bidding already exists.', message)
    @api.response(400, 'Bad request.', bad_request)
    @api.expect(bidding_input)
    def post(self):
        """
        Adds a new bidding
        """
        data = request.json
        id = add_bidding(data)
        return {"location": f"{api.base_url}biddings/{id}"}, 201


@api.response(404, 'Biddings not found', message)
@biddings_namespace.route('/<string:email>')
class ProjectCollection(Resource):
    @api.marshal_list_with(bidding_output)
    @api.response(200, 'Projects successfully queried.')
    def get(self, email):
        """
        Returns all biddings under email specified.
        """
        return get_biddings_by_email(email)


@api.response(404, 'Bidding not found', message)
@biddings_namespace.route('/<int:id>')
class BiddingItem(Resource):

    @api.marshal_with(bidding_output)
    @api.response(200, 'Biddings successfully queried.')
    def get(self, id):
        """
        Return a single bidding
        """
        return get_bidding(id)

    @api.response(200, 'Bidding successfully deleted.', message)
    def delete(self, id):
        """
        Deletes a single bidding
        """
        delete_bidding(id)
        return {'message': f'Bidding with id {id} succesfully deleted '}, 200
