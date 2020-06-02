from flask_restplus import fields
from api.restplus import api

location = api.model('Resource Location', {
    'location': fields.String(required=True)
})

message = api.model('Message', {
    'message': fields.String(required=True)
})

bad_request = api.inherit('Bad request', message, {

    'erorrs': fields.Wildcard(fields.String)
})

category_output = api.model('Category Output', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True, description='Category name')
})

category_input = api.model('Category Input', {
    'name': fields.String(required=True, description='Category name')
})

attachment_input = api.model('Attachment Input', {
    'user_email': fields.String(required=True),
    'job_id': fields.Integer(required=True),
    'file_name': fields.String(required=True),
    'file_type': fields.String(required=True, enum=['.txt', '.zip', '.png', '.jpg', '.jpeg']),
    'content_as_string': fields.String(required=True),
    'created_at': fields.DateTime(required=False)
})

attachment_output = api.model('Attachment Output', {
    'id': fields.Integer(required=True),
    'job_id': fields.Integer(required=True),
    'file_name': fields.String(required=True),
    'link': fields.String(required=True),
    'created_at': fields.String(required=True)
})

job_input = api.model('Job Input', {
    'user_email': fields.String(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'payment': fields.Fixed(decimals=5, required=True),
    'created_at': fields.DateTime(required=False),
    'category_id': fields.String(attribute='category.id', required=True)
})

job_output = api.model('Job Ouput', {
    'id': fields.Integer(required=True),
    'user_email': fields.String(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'payment': fields.Fixed(decimals=5, required=True),
    'created_at': fields.DateTime(required=True),
    'category': fields.Nested(category_output, required=True)
})

job_output_complete = api.inherit('Job Output Complete', job_output, {
    'attachments': fields.List(fields.Nested(attachment_output))
} )



marketplace_file = api.model('Marketplace File', {
    'file_name': fields.String(required=True),
    'file_type': fields.String(required=True, enum=['.txt', '.zip', '.png', '.jpg', '.jpeg']),
    'content_as_string': fields.String(required=True)
})

file_output = api.model('File Output', {
    'id': fields.Integer(required=True),
    'file_name': fields.String(required=True),
    'link': fields.String(required=True)
})

