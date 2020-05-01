import datetime
import logging
import os

import google.oauth2.id_token
from flask import Flask, render_template, request
from google.auth.transport import requests
from google.cloud import datastore


class App(Flask):
    def __init__(self, import_name):
        super().__init__(import_name,
                         static_url_path='',
                         static_folder=os.path.join(os.getcwd(), 'web', 'static'),
                         template_folder=os.path.join(os.getcwd(), 'web', 'templates', 'public'))

        self.data_store_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

        self.add_url_rule('/', view_func=self.root, methods=['GET', 'POST'])
        self.register_error_handler(500, self.server_error)

    def store_time(self, dt):
        entity = datastore.Entity(key=self.data_store_client.key('visit'))
        entity.update({
            'timestamp': dt
        })

        self.data_store_client.put(entity)

    def fetch_times(self, limit):
        query = self.data_store_client.query(kind='visit')
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
            except ValueError as exc:
                # This will be raised if the token is expired or any other
                # verification checks fail.
                error_message = str(exc)

            # Record and fetch the recent times a logged-in user has accessed
            # the site. This is currently shared amongst all users, but will be
            # individualized in a following step.
            self.store_time(datetime.datetime.now())
            times = self.fetch_times(10)

        return render_template(
            'index.html',
            user_data=claims, error_message=error_message, times=times)

    # [END gae_python37_auth_verify_token]

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
