import firebase_admin
from user.models import User
from firebase_admin import auth
from firebase_admin import credentials, exceptions
from rest_framework import authentication

from .exceptions import *

from django.conf import settings


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": settings.FIREBASE_PROJECT_ID,
  "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
  "private_key":settings.FIREBASE_PRIVATE_KEY,
  "client_email": settings.FIREBASE_CLIENT_EMAIL,
  "client_id": settings.FIREBASE_CLIENT_ID,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": settings.FIREBASE_CLIENT_CERT,
  "universe_domain": "googleapis.com"
})
default_app = firebase_admin.initialize_app(cred)