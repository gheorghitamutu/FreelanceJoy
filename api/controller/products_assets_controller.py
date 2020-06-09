import base64
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from api.utilities.files_utility import GCloudStorage
from api.controller.projects_controller import get_project
from api.controller.marketplace_controller import get_marketplace_project
from api.database.models import ProductAsset, db
from config import BUCKET_NAME

log = logging.getLogger(__name__)
storage_manager = GCloudStorage(log, BUCKET_NAME)
storage_root_directory = "marketplace/assets"


def get_asset(image_id):
    try:
        return ProductAsset.query.filter(ProductAsset.id == image_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Presentation image with id {image_id} doesn't exist") from e


def add_asset(data, file):
    file_path = f"{storage_root_directory}/{data['project_for_sale_id']}/{data['file_name']}"
    try:
        if storage_manager.check_file_existence(file_path) is False:
            link = storage_manager.upload_file(file_path, file, data['file_type'])
            if link:
                product_asset = ProductAsset()
                get_marketplace_project(data['project_for_sale_id'])

                del data['file_type']
                data['link'] = link
                for key in data:
                    setattr(product_asset, key, data[key])
                db.session.add(product_asset)
                db.session.commit()
                return product_asset.id
        else:
            raise IntegrityError(None, None, None)
    except IntegrityError as e:
        storage_manager.delete_file(file_path)
        raise IntegrityError(f"Product asset with name {data['file_name']} already exists", None, None) from e


def delete_asset(asset_id):
    existent_asset = get_asset(asset_id)
    if existent_asset:
        db.session.delete(existent_asset)
        storage_manager.delete_file(existent_asset.link.split("appspot.com/")[1])
        db.session.commit()
