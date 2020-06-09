import logging
import traceback

from flask_restx import Api
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import MethodNotAllowed
log = logging.getLogger(__name__)

api = Api(version='1.0', title='freelanceJoy API',
          description='Flask RestPlus powered API')


@api.errorhandler(MethodNotAllowed)
def method_not_allowed(e):
    log.error(e)
    return {'message': 'Method not allowed'}, 405



@api.errorhandler(NoResultFound)
def database_result_not_found_error_handler(e):
    log.exception( e.args[0])
    return {'message': e.args[0]}, 404

@api.errorhandler(IntegrityError)
def integrity_error_handler(e):
    log.exception(e)
    log.info(e.statement)
    return {'message': e.statement}, 409



@api.errorhandler
def default_error_handler(e):
    message = 'Server error'
    log.info(message)
    log.exception(e)
    return {'message': message}, 500
