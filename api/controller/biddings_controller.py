from sqlalchemy.orm.exc import NoResultFound

from api.controller.jobs_controller import check_job_existence
from api.database.models import Bidding, db


def add_bidding(bidding_obj):
    check_job_existence(bidding_obj['job_id'])
    bidding = Bidding()
    for key in bidding_obj:
        setattr(bidding, key, bidding_obj[key])
    db.session.add(bidding)
    db.session.commit()
    return bidding.id


def get_bidding(bidding_id):
    try:
        return Bidding.query.filter(Bidding.id == bidding_id).one()
    except NoResultFound as e:
        raise NoResultFound(f"Bidding with id {bidding_id} doesn't exist") from e


def delete_bidding(bidding_id):
    bidding = get_bidding(bidding_id)
    db.session.delete(bidding)
    db.session.commit()
