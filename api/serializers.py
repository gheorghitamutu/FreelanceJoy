from flask_restplus import fields
from api.restplus import api

category_output = api.model('Category Output', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True, description='Category name')
})


category_input = api.model('Category Input', {
    'name': fields.String(required=True, description='Category name')
})

