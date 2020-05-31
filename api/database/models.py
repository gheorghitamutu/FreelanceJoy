from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    # category = db.relationship('Job', backref=db.backref('categories', lazy='select'))
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Category {}".format(self.name)

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    title = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    payment = db.Column(db.Numeric(precision=5, scale=2))
    created_at = db.Column(db.TIMESTAMP)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('jobs', lazy='dynamic'))

    def __init__(self, category=None, user_email=None, title=None, description=None, payment=None, created_at=None):
        self.user_email = user_email
        self.title = title
        self.description = description
        self.payment = payment
        self.category = category
        self.created_at = created_at

    def __repr__(self):
        return "Job {}".format(self.title)

class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    def __init__(self, link):
        self.link = link

    def __repr__(self):
        return "Attachment {}".format(self.id)