import logging
from api.database.models import Attachment, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from api.controller.jobs_controller import check_job_existence
from sqlalchemy.orm.exc import NoResultFound
from api.controller.files_utility import GCloudStorage
from config import BUCKET_NAME


log = logging.getLogger(__name__)
storage_manager = GCloudStorage(log, BUCKET_NAME)
storage_root_directory = "freelance"
attachments_directory = "attachment"


def check_attachment_existence(attachment_id):
    try:
        return Attachment.query.filter(Attachment.id == attachment_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Attachment with id {attachment_id} doesn't exist") from e


def get_attachment(attachment_id):
    return check_attachment_existence(attachment_id)


def add_attachment(data):
    file_path = f"{storage_root_directory}/{data['user_email']}/{data['job_id']}/{attachments_directory}/{data['file_name']}"
    try:
        if storage_manager.check_file_existence(file_path) is False:
            link = storage_manager.upload_file(file_path, data['content_as_string'], data['file_type'])
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
    existent_attachment = check_attachment_existence(attachment_id)
    if existent_attachment:
        db.session.delete(existent_attachment)
        storage_manager.delete_file(existent_attachment.link.split("appspot.com/")[1])
        db.session.commit()
