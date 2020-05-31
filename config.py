from google.cloud import datastore, secretmanager
from flask import json
from firebase_admin import credentials

secrets = secretmanager.SecretManagerServiceClient()


CLIENT_SECRET = \
    json.loads(secrets.access_secret_version("projects/927858267242/secrets/CLIENT_SECRET/versions/1")
               .payload.data.decode("utf-8"))
FIREBASE_ADMIN_SECRET = \
    json.loads(
        secrets.access_secret_version("projects/927858267242/secrets/FIREBASE_ADMIN_SECRET/versions/1") \
            .payload.data.decode("utf-8"))

FIREBASE_ADMIN_CREDENTIALS = credentials.Certificate(FIREBASE_ADMIN_SECRET)

DATABASE_SECRET = \
    secrets.access_secret_version("projects/927858267242/secrets/SQL_AUTH_DETAILS/versions/5") \
        .payload.data.decode("utf-8")

# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:hello@127.0.0.1:3306/freelancejoy"
SQLALCHEMY_DATABASE_URI = DATABASE_SECRET
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_TIMEOUT = 100
SQLALCHEMY_MAX_OVERFLOW = 10

SWAGGER_UI_DOC_EXPANSION = "list"
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
ERROR_404_HELP = True
