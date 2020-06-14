import datetime
import json
import logging
import os
from functools import wraps

import firebase_admin
import google.oauth2.credentials
import google.oauth2.id_token
import requests
from firebase_admin import auth
from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_caching import Cache
from flask_sitemap import Sitemap, sitemap_page_needed
from google.auth.transport import requests as google_requests
from google.cloud import datastore
from werkzeug.middleware.proxy_fix import ProxyFix

from api.database.models import db
from api.endpoints.attachments_endpoing import attachments_namespace
from api.endpoints.biddings_endpoint import biddings_namespace
from api.endpoints.categories_endpoint import categories_namespace
from api.endpoints.delivered_assets_endpoint import projects_assets_namespace
from api.endpoints.jobs_endpoint import jobs_namespace
from api.endpoints.marketplace_endpoint import marketplace_namespace
from api.endpoints.product_assets_endpoint import assets_namespace
from api.endpoints.projects_endpoint import projects_namespace
from api.restplus import api
from config import *

os.environ.setdefault("GCLOUD_PROJECT", "freelancejoy")


class App(Flask):
    def __init__(self, import_name):
        super().__init__(import_name,
                         static_url_path='',
                         static_folder=os.path.join(os.getcwd(), 'web', 'static'),
                         template_folder=os.path.join(os.getcwd(), 'web', 'templates', 'public'))
        self.wsgi_app = ProxyFix(self.wsgi_app)
        self.data_store_client = datastore.Client()
        self.client_secret = CLIENT_SECRET
        self.firebase_admin_secret = FIREBASE_ADMIN_SECRET
        self.firebase_admin_credentials = FIREBASE_ADMIN_CREDENTIALS
        firebase_admin.initialize_app(self.firebase_admin_credentials)

        # database

        self.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        self.config["SQLALCHEMY_ECHO"] = SQLALCHEMY_ECHO
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
        self.config["SQLALCHEMY_POOL_TIMEOUT"] = SQLALCHEMY_POOL_TIMEOUT
        self.config["SQLALCHEMY_MAX_OVERFLOW"] = SQLALCHEMY_MAX_OVERFLOW
        self.config['SWAGGER_UI_DOC_EXPANSION'] = SWAGGER_UI_DOC_EXPANSION
        self.config['RESTPLUS_VALIDATE'] = RESTPLUS_VALIDATE
        self.config['RESTPLUS_MASK_SWAGGER'] = RESTPLUS_MASK_SWAGGER
        self.config['ERROR_404_HELP'] = ERROR_404_HELP

        self.db = db
        self.db.init_app(self)
        self.app_context().push()

        with self.app_context():
            self.db.create_all()  # Create database tables for our data models

        self.flow = None
        self.session = dict()

        self.cache = Cache(app=self, config={'CACHE_TYPE': 'simple'})
        self.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = False  # true for listing every route available
        self.flask_sitemap = Sitemap(app=self)
        # keep a sitemap only for the pages that does not require authentication (may add special cases later)
        self.flask_sitemap.register_generator(self.root_sitemap)

        self.add_url_rule('/', view_func=self.landing, methods=['GET'])
        self.add_url_rule('/dashboard', view_func=self.dashboard, methods=['GET'])
        self.add_url_rule('/my_projects', view_func=self.my_projects, methods=['GET'])
        self.add_url_rule('/my_jobs', view_func=self.my_jobs, methods=['GET'])
        self.add_url_rule('/see_job/<int:job_id>', view_func=self.see_job, methods=['GET'])
        self.add_url_rule('/delete_job/<int:job_id>', view_func=self.delete_job, methods=['GET'])
        self.add_url_rule('/logout', view_func=self.logout, methods=['GET'])
        self.add_url_rule('/login', view_func=self.login, methods=['GET'])

        # APIs endpoints
        blueprint = Blueprint('api', __name__, url_prefix='/api')
        api.init_app(blueprint)
        api.add_namespace(categories_namespace)
        api.add_namespace(jobs_namespace)
        api.add_namespace(attachments_namespace)
        api.add_namespace(biddings_namespace)
        api.add_namespace(projects_namespace)
        api.add_namespace(projects_assets_namespace)
        api.add_namespace(marketplace_namespace)
        api.add_namespace(assets_namespace)
        self.register_blueprint(blueprint)

        self.register_error_handler(500, self.server_error)
        self.register_error_handler(404, self.not_found)

    def store_time(self, email, dt):
        entity = datastore.Entity(key=self.data_store_client.key('User', email, 'visit'))
        entity.update({
            'timestamp': dt
        })

        self.data_store_client.put(entity)

    def fetch_times(self, email, limit):
        ancestor = self.data_store_client.key('User', email)
        query = self.data_store_client.query(kind='visit', ancestor=ancestor)
        query.order = ['-timestamp']

        times = query.fetch(limit=limit)

        return times

    def landing(self):
        return render_template('index.html')

    @staticmethod
    def root_sitemap():
        # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
        yield 'landing', {}

    def get_claim(self):
        # Verify Firebase auth.
        id_token = request.cookies.get("token")
        error_message = None
        claims = None
        times = None

        if id_token:
            try:
                # Verify the token against the Firebase Auth API. This example
                # verifies the token on each page load. For improved performance,
                # some applications may wish to cache results in an encrypted
                # session store (see for instance
                claims = google.oauth2.id_token.verify_firebase_token(id_token, google_requests.Request())

                if 'current_user' not in self.session:
                    self.session['current_user'] = dict()

                sign_in_provider = claims['firebase']['sign_in_provider']
                if sign_in_provider == 'phone':
                    self.store_time(claims['phone_number'], datetime.datetime.now())
                    times = self.fetch_times(claims['phone_number'], 10)
                    userInfo = auth.get_user_by_phone_number(claims['phone_number'])
                else:
                    self.store_time(claims['email'], datetime.datetime.now())
                    times = self.fetch_times(claims['email'], 10)
                    userInfo = auth.get_user_by_email(claims['email'])

                self.session['claims'] = claims

                self.session['current_user']['uid'] = userInfo.uid
                self.session['current_user']['phone_number'] = userInfo.phone_number
                self.session['current_user']['email'] = userInfo.email
                self.session['current_user']['provider_id'] = userInfo.provider_id
                self.session['current_user']['disabled'] = userInfo.disabled
                self.session['current_user']['tokens_valid_after_timestamp'] = userInfo.tokens_valid_after_timestamp
                self.session['current_user']['creation_timestamp'] = userInfo.user_metadata.creation_timestamp
                self.session['current_user']['last_sign_in_timestamp'] = userInfo.user_metadata.last_sign_in_timestamp
                self.session['current_user']['provider_data'] = userInfo.provider_data
                self.session['current_user']['custom_claims'] = userInfo.custom_claims
                self.session['current_user']['tenant_id'] = userInfo.tenant_id

            except ValueError as exc:
                # This will be raised if the token is expired or any other
                # verification checks fail.
                error_message = str(exc)

        return claims, times, error_message

    def login_required(func):
        @wraps(func)
        def function_wrapper(*args):
            if 'claims' in args[0].session:
                claims = args[0].session['claims']
                if claims is not None and datetime.datetime.now().timestamp() < claims['exp']:
                    claims, times, error_message = args[0].get_claim()
                    if error_message is None:
                        return func(*args)

                args[0].session = dict()
                return args[0].unauthorized_handler()
            else:
                return args[0].unauthorized_handler()

        return function_wrapper

    def login(self):
        claims, times, error_message = self.get_claim()
        if error_message is None and claims is not None:
            return redirect(url_for('dashboard'), code=302)

        return render_template('login.html')

    @login_required
    def logout(self):
        auth.revoke_refresh_tokens(self.session['current_user']['uid'])
        self.session = dict()
        return redirect(url_for('login'))

    @login_required
    def dashboard(self):
        project_list = self.get_user_project_list(request.url_root, self.session['claims']['email'])
        projects_count = len(project_list)
        projects_past_deadline_count = \
            len(list(filter(
                lambda p: datetime.datetime.strptime(p['deadline'], '%Y-%m-%dT%H:%M:%S') < datetime.datetime.now(),
                project_list)))
        projects_in_progress = projects_count

        bidding_list = self.get_user_bidding_list(request.url_root, self.session['claims']['email'])
        biddings_count = len(bidding_list)

        jobs_list = self.get_user_job_list(request.url_root, self.session['claims']['email'])
        jobs_count = len(jobs_list)

        user_data = {
            'projects_count': projects_count,
            'projects_past_deadline': projects_past_deadline_count,
            'projects_in_progress': projects_in_progress,
            'biddings_count': biddings_count,
            'jobs_count': jobs_count
        }

        return render_template('dashboard.html', session=self.session, user_data=user_data)

    @login_required
    def my_projects(self):
        project_list = self.get_user_project_list(request.url_root, self.session['claims']['email'])
        return render_template('my_projects.html', session=self.session, project_list=project_list)

    @login_required
    def my_jobs(self):
        job_list = self.get_user_job_list(request.url_root, self.session['claims']['email'])
        return render_template('my_jobs.html', session=self.session, job_list=job_list)

    def see_job(self, job_id):
        job = self.get_job(request.url_root, job_id)

        return render_template('job.html', session=self.session, job=job)

    def delete_job(self, job_id):
        self.delete_user_job(request.url_root, job_id)

        return redirect(url_for('dashboard'))

    @staticmethod
    def delete_user_job(url_root, job_id):
        api_url = '{}api/jobs/{}'.format(url_root, job_id)
        # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        r = requests.delete(api_url, verify=False)

        return r

    @staticmethod
    def get_job(url_root, job_id):
        api_url = '{}api/jobs/{}'.format(url_root, job_id)
        # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        r = requests.get(api_url, verify=False)
        job = json.loads(r.text)

        return job

    @staticmethod
    def get_user_job_list(url_root, email):
        api_url = '{}api/jobs/?page=1&per_page=50&user_email={}&freelancer_flag=false'.format(url_root, email)
        # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        r = requests.get(api_url, verify=False)
        job_list = json.loads(r.text)

        return job_list['items']

    @staticmethod
    def get_user_project_list(url_root, email):
        api_url = '{}api/projects/{}'.format(url_root, email)
        # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        r = requests.get(api_url, verify=False)
        project_list = json.loads(r.text)

        return project_list

    @staticmethod
    def get_user_bidding_list(url_root, email):
        api_url = '{}api/biddings/{}'.format(url_root, email)
        # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        r = requests.get(api_url, verify=False)
        bidding_list = json.loads(r.text)

        return bidding_list

    @staticmethod
    def unauthorized_handler():
        return redirect(url_for('login'))

    @staticmethod
    def not_found(e):
        return str(e)

    @staticmethod
    def server_error(e):
        logging.exception('An error occurred during a request.')
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    @sitemap_page_needed.connect
    def create_page(self, page, urlset):
        self.cache[page] = self.flask_sitemap.render_page(urlset=urlset)

    def load_page(self, fn):
        @wraps(fn)
        def loader(*args, **kwargs):
            page = kwargs.get('page')
            data = self.cache.get(page)
            return data if data else fn(*args, **kwargs)

        return loader


app = App(__name__)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, ssl_context='adhoc')
