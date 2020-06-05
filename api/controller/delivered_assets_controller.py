import base64
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.utilities.files_utility import GCloudStorage
from api.controller.projects_controller import get_project
from api.controller.jobs_controller import get_job
from api.database.models import DeliveredProjectAsset, db
from config import BUCKET_NAME

log = logging.getLogger(__name__)
storage_manager = GCloudStorage(log, BUCKET_NAME)
storage_root_directory = "freelance"
directory = "project"


def get_delivered_project_asset(delivered_project_asset_id):
    try:
        return DeliveredProjectAsset.query.filter(DeliveredProjectAsset.id == delivered_project_asset_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"delivered_project_asset with id {delivered_project_asset_id} doesn't exist") from e


def add_delivered_project_asset(data):
    file_path = f"{storage_root_directory}/{data['employer_email']}/{data['job_id']}/{directory}/{data['file_name']}"
    try:
        if storage_manager.check_file_existence(file_path) is False:
            content = base64.b64decode(data['content_as_string'])
            link = storage_manager.upload_file(file_path, content, data['file_type'])
            if link:
                delivered_project_asset = DeliveredProjectAsset()
                get_project(data['project_id'])
                get_job(data['job_id'])

                del data['file_type'], data['user_email'], data['job_id']
                data['link'] = link
                for key in data:
                    setattr(delivered_project_asset, key, data[key])
                db.session.add(delivered_project_asset)
                db.session.commit()
                return delivered_project_asset.id
        else:
            raise IntegrityError(None, None, None)
    except IntegrityError as e:
        storage_manager.delete_file(file_path)
        raise IntegrityError(f"delivered_project_asset with name {data['file_name']} already exists", None, None) from e


def delete_delivered_project_asset(delivered_project_asset_id):
    existent_delivered_project_asset = get_delivered_project_asset(delivered_project_asset_id)
    if existent_delivered_project_asset:
        db.session.delete(existent_delivered_project_asset)
        storage_manager.delete_file(existent_delivered_project_asset.link.split("appspot.com/")[1])
        db.session.commit()
