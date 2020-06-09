from flask_restx import fields
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

generic_file_output = api.model('Generic File Output', {
    'id': fields.Integer(required=True),
    'file_name': fields.String(required=True),
    'link': fields.String(required=True),
    'created_at': fields.String(required=True)
})

attachment_output = api.inherit('Attachment Output', generic_file_output, {
    'job_id': fields.Integer(required=True)
})

delivered_project_asset_output = api.inherit('Project Asset Output', generic_file_output, {
    'id': fields.Integer(required=True),
    'project_id': fields.Integer(required=True),
    'message': fields.String(required=True)
})

product_asset_output = api.inherit('Product Asset Input', generic_file_output, {
    'id': fields.Integer(required=True),
    'asset_type': fields.String(required=True)
})

bidding_input = api.model('Bidding Input', {
    'freelancer_email': fields.String(required=True),
    'message': fields.String(required=True),
    'created_at': fields.DateTime(required=False),
    'job_id': fields.Integer(required=True)
})

bidding_output = api.inherit('Bidding Output', bidding_input, {
    'id': fields.Integer(required=True),
    'created_at': fields.DateTime(required=True),
})

project_input = api.model('Project Input', {
    'deadline': fields.DateTime(required=True),
    'freelancer_email': fields.String(required=True),
    'job_id': fields.Integer(required=True),
    'created_at': fields.DateTime(required=False)

})

project_output = api.inherit('Project Ouput', project_input, {
    'id': fields.Integer(required=True)
})

job_input = api.model('Job Input', {
    'user_email': fields.String(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'payment': fields.Float(required=True),
    'created_at': fields.DateTime(required=False),
    'category_id': fields.Integer(required=True)
})

job_output = api.model('Job Ouput', {
    'id': fields.Integer(required=True),
    'user_email': fields.String(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'payment': fields.Float(required=True),
    'created_at': fields.DateTime(required=True),
    # 'category': fields.Nested(category_output, required=True),
    'attachments': fields.List(fields.Nested(attachment_output)),
    'biddings': fields.List(fields.Nested(bidding_output)),
    'project': fields.Nested(project_output)
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_jobs = api.inherit('Page of jobs', pagination, {
    'items': fields.List(fields.Nested(job_output))
})

marketplace_project_input = api.model('Marketplace Project Input', {
    'user_email': fields.String(required=True),
    'partner_email': fields.String(required=False),
    'category_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Fixed(decimals=2, required=True),
    'created_at': fields.DateTime(required=False)
})

marketplace_project_output = api.model('Marketplace Project Output', {
    'id': fields.Integer(required=True),
    'created_at': fields.DateTime(required=True),
    'assets_archive_link': fields.String(required=True),
    'assets': fields.List(fields.Nested(product_asset_output), required=True),
    'user_email': fields.String(required=True),
    'partner_email': fields.String(required=False),
    'category_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Fixed(decimals=2, required=True),
})

page_of_marketplace_projects = api.inherit('Page of marketplace items', pagination, {
    'items': fields.List(fields.Nested(marketplace_project_output), required=True)
})
