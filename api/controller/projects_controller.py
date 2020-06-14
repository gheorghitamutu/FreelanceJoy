from sqlalchemy.orm.exc import NoResultFound

from api.controller.jobs_controller import get_job
from api.database.models import db, Project


def get_project_by_id(project_id):
    try:
        return Project.query.filter(Project.id == project_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Project with id {project_id} doesn't exist") from e


def get_projects_by_email(freelancer_email):
    try:
        return Project.query.filter(Project.freelancer_email == freelancer_email).all()
    except NoResultFound as e:
        raise NoResultFound(f"Projects for freelancer email {freelancer_email} don't exist") from e


def add_project(project_obj):
    get_job(project_obj['job_id'])
    project = Project()
    for key in project_obj:
        setattr(project, key, project_obj[key])
    db.session.add(project)
    db.session.commit()
    return project.id


def delete_project(project_id):
    project = get_project_by_id(project_id)
    db.session.delete(project)
    db.session.commit()