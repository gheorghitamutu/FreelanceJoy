from flask_restplus import fields
from api.restplus import api

category = api.model('Category', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True, description='Category name')
})

category_array = api.model('Categories array', {
    'categories': fields.List(required=True, description='Category list', cls_or_instance=fields.Nested(category))
})

id = api.model('General id', {
    'id' : fields.Integer(required=True)
})

ids =  api.model('Ids array', {
    'ids': fields.List(required=True, description='Category list', cls_or_instance=fields.Nested(id))
})
