import logging

from api.database.models import Job, db
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


def check_job_existence(job_id):
    try:
        return Job.query.filter(Job.id == job_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Job with id {job_id} doesn't exist") from e


def add_job(job_obj):
    job = Job()
    for key in job_obj:
        setattr(job, key, job_obj[key])
    db.session.add(job)
    db.session.commit()
    return job.id


def get_jobs():
    return Job.query.all()


def get_job(job_id):
    return check_job_existence(job_id)

def delete_job(job_id):
    db.session.delete(check_job_existence(job_id))
    db.session.commit()
