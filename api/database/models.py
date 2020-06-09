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

    project = db.relationship('Project', backref=db.backref('jobs', lazy=False))

    biddings = db.relationship('Bidding', backref=db.backref('jobs', lazy=True))
    attachments = db.relationship('Attachment', backref=db.backref('jobs', lazy=True))

    def __init__(self, user_email=None, title=None, description=None,
                 payment=None,
                 created_at=None):
        self.user_email = user_email
        self.title = title
        self.description = description
        self.payment = payment
        self.created_at = created_at

    def __repr__(self):
        return "Job {}".format(self.title)


class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    file_name = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    def __init__(self, link=None, file_name=None, created_at=None):
        self.link = link
        self.file_name = file_name
        self.created_at = created_at

    def __repr__(self):
        return "Attachment {}".format(self.name)


class DeliveredProjectAsset(db.Model):
    __tablename__ = "projects_delivered_assets"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    file_name = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    message = db.Column(db.String)

    def __init__(self, link=None, file_name=None, created_at=None):
        self.link = link
        self.file_name = file_name
        self.created_at = created_at

    def __repr__(self):
        return "Delivered project asset {}".format(self.name)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    deadline = db.Column(db.TIMESTAMP)
    freelancer_email = db.Column(db.String)
    created_at = db.Column(db.String)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    delivered_assets = db.relationship('DeliveredProjectAsset', backref=db.backref('projects', lazy=True))

    def __init__(self, deadline=None, freelancer_email=None, created_at=None):
        self.deadline = deadline
        self.freelancer_email = freelancer_email
        self.created_at = created_at

    def __repr__(self):
        return "Project {}".format(self.id)


class Bidding(db.Model):
    __tablename__ = "biddings"
    id = db.Column(db.Integer, primary_key=True)
    freelancer_email = db.Column(db.String)
    message = db.Column(db.TEXT)
    created_at = db.Column(db.TIMESTAMP)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    def __init__(self, freelancer_email=None, message=None, created_at=None):
        self.freelancer_email = freelancer_email
        self.message = message
        self.created_at = created_at

    def __repr__(self):
        return "Bidding {}".format(self.id)


class MarketplaceProject(db.Model):
    __tablename__ = "projects_for_sale"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    partner_email = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Numeric(precision=5, scale=2))
    description = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    assets = db.relationship('ProductAsset', backref=db.backref('projects_for_sale', lazy=True))


class ProductAsset(db.Model):
    __tablename__ = "projects_for_sale_assets"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    link = db.Column(db.String)
    project_for_sale_id = db.Column(db.Integer, db.ForeignKey('projects_for_sale.id'))
    asset_type = db.Column(db.Enum('image', 'archive'))
    created_at = db.Column(db.DateTime)
