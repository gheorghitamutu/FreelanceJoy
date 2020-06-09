import base64
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.utilities.files_utility import GCloudStorage
from api.controller.jobs_controller import check_job_existence
from api.database.models import Attachment, db
from config import BUCKET_NAME

log = logging.getLogger(__name__)
storage_manager = GCloudStorage(log, BUCKET_NAME)
storage_root_directory = "freelance"
attachments_directory = "attachment"


def get_attachment(attachment_id):
    try:
        return Attachment.query.filter(Attachment.id == attachment_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Attachment with id {attachment_id} doesn't exist") from e


def add_attachment(file, data):
    file_path = f"{storage_root_directory}/{data['user_email']}/{data['job_id']}/{attachments_directory}/{data['file_name']}"
    try:
        if storage_manager.check_file_existence(file_path) is False:
            link = storage_manager.upload_file(file_path, file, data['file_type'])
            if link:
                attachment = Attachment()
                check_job_existence(data['job_id'])
                del data['file_type'], data['user_email']
                data['link'] = link
                for key in data:
                    setattr(attachment, key, data[key])
                db.session.add(attachment)
                db.session.commit()
                return attachment.id
        else:
            raise IntegrityError(None, None, None)
    except IntegrityError as e:
        storage_manager.delete_file(file_path)
        raise IntegrityError(f"Attachment with name {data['file_name']} already exists", None, None) from e


def delete_attachment(attachment_id):
    existent_attachment = get_attachment(attachment_id)
    if existent_attachment:
        db.session.delete(existent_attachment)
        storage_manager.delete_file(existent_attachment.link.split("appspot.com/")[1])
        db.session.commit()
