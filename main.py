import os

os.environ.setdefault("GCLOUD_PROJECT", "freelancejoy")

import datetime
import logging
import os
from functools import wraps
from urllib.parse import urlparse

import firebase_admin
import google.oauth2.credentials
import google.oauth2.id_token
from firebase_admin import auth, credentials
from flask import Flask, render_template, request, json, redirect, url_for
from flask_caching import Cache
from flask_sitemap import Sitemap, sitemap_page_needed
from google.auth.transport import requests as google_requests
from google.cloud import datastore, secretmanager
from google_auth_oauthlib.flow import Flow


class App(Flask):
    def __init__(self, import_name):
        super().__init__(import_name,
                         static_url_path='',
                         static_folder=os.path.join(os.getcwd(), 'web', 'static'),
                         template_folder=os.path.join(os.getcwd(), 'web', 'templates', 'public'))

        self.data_store_client = datastore.Client()
        self.secrets = secretmanager.SecretManagerServiceClient()
        self.client_secret = \
            json.loads(self.secrets.access_secret_version("projects/927858267242/secrets/CLIENT_SECRET/versions/1")
                       .payload.data.decode("utf-8"))
        self.firebase_admin_secret = \
            json.loads(
                self.secrets.access_secret_version("projects/927858267242/secrets/FIREBASE_ADMIN_SECRET/versions/1")
                    .payload.data.decode("utf-8"))

        self.firebase_admin_credentials = credentials.Certificate(self.firebase_admin_secret)
        firebase_admin.initialize_app(self.firebase_admin_credentials)

        self.flow = None
        self.session = dict()

        self.cache = Cache(app=self, config={'CACHE_TYPE': 'simple'})
        self.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = False  # true for listing every route available
        self.flask_sitemap = Sitemap(app=self)
        # keep a sitemap only for the pages that does not require authentication (may add special cases later)
        self.flask_sitemap.register_generator(self.root_sitemap)

        self.add_url_rule('/', view_func=self.root, methods=['GET'])
        # currently not used
        self.add_url_rule('/google_login', view_func=self.google_login, methods=['GET'])
        # currently not used
        self.add_url_rule('/__/auth/handler/', view_func=self.handle_auth, methods=['GET'])
        self.add_url_rule('/dashboard', view_func=self.dashboard, methods=['GET'])
        self.add_url_rule('/logout', view_func=self.logout, methods=['GET'])

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

    def root(self):
        claims, times, error_message = self.get_claim()
        if error_message is None and claims is not None:
            return redirect(url_for('dashboard'), code=302)

        return render_template('landing.html')

    @staticmethod
    def root_sitemap():
        # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
        yield 'root', {}

    def google_login(self):
        # onclick="location.href='{{ url_for('google_login') }}'"
        # currently not used because you can't get an ID token from server side Firebase

        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        self.flow = Flow.from_client_config(
            self.client_secret,
            scopes=['openid',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email'])

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        url_parsed = urlparse(request.base_url)
        self.flow.redirect_uri = '{}://{}/__/auth/handler/'.format(url_parsed.scheme, url_parsed.netloc)

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = self.flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        return redirect(authorization_url)

    def handle_auth(self):
        cred = self.flow.fetch_token(authorization_response=request.url)
        authorized_session = self.flow.authorized_session()
        response = authorized_session.get('https://www.googleapis.com/userinfo/v2/me')

        self.session['current_user'] = json.loads(response.content.decode('utf-8').replace("'", '"'))  # bad
        self.session['credentials'] = cred  # super bad

        user = {
            'display_name': self.session['current_user']['name'],
            'email': self.session['current_user']['email'],
            'email_verified': self.session['current_user']['verified_email'],
            'phone_number': None,
            'photo_url': self.session['current_user']['picture'],
            'password': None,
            'disabled': False,
            'app': None
        }

        try:
            userInfo = auth.get_user_by_email(self.session['current_user']['email'])
            userInfo = auth.update_user(userInfo.uid, **user)  # may want to add info from here
        except Exception as e:
            print(e)
            userInfo = auth.create_user(**user)

        self.session['current_user']['uid'] = userInfo.uid
        self.session['current_user']['phone_number'] = userInfo.phone_number
        self.session['current_user']['provider_id'] = userInfo.provider_id
        self.session['current_user']['disabled'] = userInfo.disabled
        self.session['current_user']['tokens_valid_after_timestamp'] = userInfo.tokens_valid_after_timestamp
        self.session['current_user']['creation_timestamp'] = userInfo.user_metadata.creation_timestamp
        self.session['current_user']['last_sign_in_timestamp'] = userInfo.user_metadata.last_sign_in_timestamp
        self.session['current_user']['provider_data'] = userInfo.provider_data
        self.session['current_user']['custom_claims'] = userInfo.custom_claims
        self.session['current_user']['tenant_id'] = userInfo.tenant_id

        return redirect(url_for('dashboard'))

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
                if datetime.datetime.now().timestamp() < claims['exp']:
                    claims, times, error_message = args[0].get_claim()
                    if error_message is None:
                        return func(*args)

                args[0].session = dict()
                return args[0].unauthorized_handler()
            else:
                return args[0].unauthorized_handler()

        return function_wrapper

    @login_required
    def logout(self):
        auth.revoke_refresh_tokens(self.session['current_user']['uid'])
        self.session = dict()
        return redirect(url_for('root'))

    @login_required
    def dashboard(self):
        return render_template('dashboard.html', session=self.session)

    @staticmethod
    def unauthorized_handler():
        return redirect(url_for('root'))

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
