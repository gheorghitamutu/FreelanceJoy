import logging

from api.database.models import Job, Category, Attachment, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


def add_job(job_obj):
    job = Job()
    category = Category.query.filter(Category.id == job_obj['category_id']).one()
    del job_obj['category_id']
    job_obj['category'] = category
    for key in job_obj:
        setattr(job, key, job_obj[key])
    db.session.add(job)
    db.session.commit()


def get_jobs():
    return Job.query.all()
