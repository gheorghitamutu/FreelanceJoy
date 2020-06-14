import logging

from sqlalchemy.orm.exc import NoResultFound

from api.database.models import Job, db, Project

log = logging.getLogger(__name__)


def check_job_existence(job_id):
    try:
        job = Job.query.filter(Job.id == job_id).one()
        return job
    except NoResultFound as e:
        raise NoResultFound(f"Job with id {job_id} doesn't exist") from e


def add_job(job_obj):
    job = Job()
    for key in job_obj:
        setattr(job, key, job_obj[key])
    db.session.add(job)
    db.session.commit()
    return job.id


def get_jobs(page, per_page, category_id, user_email, freelancer_flag):
    if category_id is not None:
        jobs_ids_with_project = [int(project.job_id) for project in Project.query.all()]
        jobs = Job.query.filter(Job.id.notin_(jobs_ids_with_project),
                                Job.category_id == category_id).order_by(Job.created_at)
        return jobs.paginate(page, per_page, error_out=False)

    if user_email is not None:
        if freelancer_flag is True:
            jobs = Job.query.join(Project).filter(Project.freelancer_email == user_email)
            return jobs.paginate(page, per_page, error_out=False)
        else:
            return Job.query.filter(Job.user_email == user_email).paginate(page, per_page, error_out=False)

    return Job.query.paginate(page, per_page, error_out=False)


def get_job(job_id):
    job = check_job_existence(job_id)
    return job


def delete_job(job_id):
    job = check_job_existence(job_id)
    db.session.delete(job)
    db.session.commit()
