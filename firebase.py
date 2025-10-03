import firebase_admin
from User.models import User
from firebase_admin import auth
from firebase_admin import credentials, exceptions
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed


from django.conf import settings

# change the cred according to your own firebase project (firebase console -> project -> project settings)
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "YOUR-PROJECT-ID",
  "private_key_id": "PRIVATE-KEY-ID",
  "private_key":"PRIVATE-KEY",
  "client_email": "CLIENT-EMAIL",
  "client_id": "CLIENT-ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR-CERT",
  "universe_domain": "googleapis.com"
})
default_app = firebase_admin.initialize_app(cred)



class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NotAuthenticated("No auth token provided")

        id_token = auth_header.split(" ").pop()
        return handle_auth(id_token,throw_error=True)
    
class FirebaseOptionalAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None

        id_token = auth_header.split(" ").pop()
        return handle_auth(id_token)

def authenticate_token(id_token):
    return handle_auth(id_token)

def handle_auth(id_token,throw_error=False):
    decoded_token = None
    try:
        decoded_token = auth.verify_id_token(id_token)        
    except Exception as err:
        if throw_error:
            print(err)
            raise AuthenticationFailed("Invalid auth token")
        else: return None

    if not id_token or not decoded_token:
        return None

    try:
        uid = decoded_token.get("uid")
    except Exception as err:
        if throw_error: raise FirebaseError()
        else: return None

    user, created = User.objects.get_or_create(firebase_uid=uid)
    return (user, None)
