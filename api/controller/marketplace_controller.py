from api.database.models import MarketplaceProject, db, Category, Project
from sqlalchemy.orm.exc import NoResultFound
from api.utilities.files_utility import GCloudStorage
from config import BUCKET_NAME
import logging
import base64

storage_root_directory = 'marketplace/products_assets'
log = logging.getLogger(__name__)
storage_manager = GCloudStorage(log, BUCKET_NAME)


def store_archive(name, content, type):
    file_path = f"{storage_root_directory}/{name}"
    if storage_manager.check_file_existence(file_path) is False:
        content = base64.b64decode(content)
        link = storage_manager.upload_file(file_path, content, type)
        return link
    return None


def get_marketplace_project(marketplace_project_id):
    try:
        return MarketplaceProject.query.filter(MarketplaceProject.id == marketplace_project_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"MarketplaceProject with id {marketplace_project_id} doesn't exist") from e


def add_marketplace_project(marketplace_project_obj):
    marketplace_project = MarketplaceProject()
    archive_name = marketplace_project_obj['assets_archive_name']
    archive_type = marketplace_project_obj['assets_archive_type']
    archive_content = marketplace_project_obj['assets_archive_content']
    del marketplace_project_obj['assets_archive_name'], marketplace_project_obj['assets_archive_type'], \
    marketplace_project_obj['assets_archive_content']
    for key in marketplace_project_obj:
        setattr(marketplace_project, key, marketplace_project_obj[key])
    setattr(marketplace_project, 'assets_archive_link', 'toBeAdded')
    db.session.add(marketplace_project)
    link = store_archive(archive_name, archive_content, archive_type)
    if link is not None:
        setattr(marketplace_project, 'assets_archive_link', link)
    db.session.commit()
    return marketplace_project.id


def get_marketplace_projects(page, per_page, category_id, user_email, freelancer_flag):
    if category_id is not None:
        marketplace_projects = MarketplaceProject.query.join(Category).order_by(MarketplaceProject.created_at)
        return marketplace_projects.paginate(page, per_page, error_out=False)

    if user_email is not None:
        if freelancer_flag is True:
            marketplace_projects = MarketplaceProject.query.filter(Project.partnet_email == user_email)
            return marketplace_projects.paginate(page, per_page, error_out=False)
        else:
            return MarketplaceProject.query.filter(MarketplaceProject.user_email == user_email).paginate(page, per_page,
                                                                                                         error_out=False)

    return MarketplaceProject.query.paginate(page, per_page, error_out=False)


def delete_marketplace_project(marketplace_project_id):
    db.session.delete(get_marketplace_project(marketplace_project_id))
    db.session.commit()
