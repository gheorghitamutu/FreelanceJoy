# https://googleapis.dev/python/datastore/latest/index.html
# https://cloud.google.com/community/tutorials/secrets-manager-python

import datetime
import logging
import os

import google.oauth2.credentials
import google.oauth2.id_token
import pyrebase
from flask import Flask, render_template, request, json, redirect
from google.auth.transport import requests
from google.cloud import datastore, secretmanager
from google_auth_oauthlib.flow import Flow


class App(Flask):
    def __init__(self, import_name):
        super().__init__(import_name,
                         static_url_path='',
                         static_folder=os.path.join(os.getcwd(), 'web', 'static'),
                         template_folder=os.path.join(os.getcwd(), 'web', 'templates', 'public'))

        self.data_store_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()
        self.secrets = secretmanager.SecretManagerServiceClient()
        self.firebase_api_key = \
            self.secrets.access_secret_version("projects/927858267242/secrets/FIREBASE_API_KEY/versions/1") \
                .payload.data.decode("utf-8")
        self.client_secret = \
            json.loads(self.secrets.access_secret_version("projects/927858267242/secrets/CLIENT_SECRET/versions/1")
                       .payload.data.decode("utf-8"))

        self.firebase_config = {
            'apiKey': self.firebase_api_key,
            'authDomain': 'freelancejoy.firebaseapp.com',
            'databaseURL': 'https://freelancejoy.firebaseio.com',
            'projectId': 'freelancejoy',
            'storageBucket': 'freelancejoy.appspot.com',
            'messagingSenderId': '927858267242',
            'appId': '1:927858267242:web:7e0e0e8251af5d80ef2613',
            'measurementId': 'G-GZE64K9308'
        }
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.firebase_auth = self.firebase.auth()
        self.firebase_db = self.firebase.database()

        self.add_url_rule('/', view_func=self.root, methods=['GET', 'POST'])
        self.add_url_rule('/login', view_func=self.login, methods=['GET', 'POST'])
        self.add_url_rule('/__/auth/handler/?<path:confirmation>', view_func=self.handle_auth, methods=['GET', 'POST'])
        self.register_error_handler(500, self.server_error)

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
                # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
                claims = google.oauth2.id_token.verify_firebase_token(
                    id_token, self.firebase_request_adapter)

                self.store_time(claims['email'], datetime.datetime.now())
                times = self.fetch_times(claims['email'], 10)
            except ValueError as exc:
                # This will be raised if the token is expired or any other
                # verification checks fail.
                error_message = str(exc)

        return render_template(
            'index.html',
            user_data=claims, error_message=error_message, times=times, firebase_config=self.firebase_config)

    # [END gae_python37_auth_verify_token]

    def login(self):
        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = Flow.from_client_config(
            self.client_secret,
            scopes=['profile', 'email'])

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = 'https://freelancejoy.firebaseapp.com/__/auth/handler'

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        return redirect(authorization_url)

    @staticmethod
    def handle_auth(confirmation):
        print(request.get('https://www.googleapis.com/userinfo/v2/me').json())
        return confirmation

    @staticmethod
    def server_error(e):
        logging.exception('An error occurred during a request.')
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500


app = App(__name__)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
