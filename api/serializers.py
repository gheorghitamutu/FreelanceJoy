from flask_restplus import fields
from api.restplus import api

category_output = api.model('Category Output', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True, description='Category name')
})


category_input = api.model('Category Input', {
    'name': fields.String(required=True, description='Category name')
})

attachment = api.model('Files', {
    'id': fields.Integer(required=False),
    'link': fields.String(required=True, description='Link to resource')
})
job = api.model('Job', {
    'id': fields.Integer(required=False),
    'user_email': fields.String(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'payment': fields.Fixed(decimals=5, required=True),
    'created_at': fields.DateTime(required=False),
    'category_id': fields.Integer(attribute='category.id'),
    'category_name': fields.String(attribute='category.name')
})

