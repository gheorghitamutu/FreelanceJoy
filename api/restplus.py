import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest, MethodNotAllowed

log = logging.getLogger(__name__)

api = Api(version='1.0', title='freelanceJoy API',
          description='Flask RestPlus powered API')


@api.errorhandler(MethodNotAllowed)
def method_not_allowed(e):
    return {'message': 'Method not allowed'}, 405


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': e.message}, 404


@api.errorhandler
def default_error_handler(e):
    message = 'Server error'
    log.error(e)
    log.exception(message)
    return {'message': message}, 500