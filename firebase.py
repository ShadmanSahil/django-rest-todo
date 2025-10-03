import firebase_admin
from User.models import User
from firebase_admin import auth
from firebase_admin import credentials, exceptions
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed


from django.conf import settings


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "fir-todo-auth-3b183",
  "private_key_id": "cb508d100675d501a1a8c4d9a0f272e3c9b201ed",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxPY1LWZSrFftH\n/qmLCbcEpBUJi2BVANc0VIG787eTRDl3YDJZ4PaTchmL8EK+VPpuMgpAYeLCt5H0\ntQhJGQNuYwOfXB86g2LDduIrBXfMTRTiYEUoVzmht3fW1n0SnHsJ2mDHZ+OR+/cs\n4XYx7LGsviQ4618p44gSmLPId26KE/vnGBkl1N9ONZUx9SBO0X80y1YR5UyignJa\nZyYGB6FDvTYKgo7ZnhYF/w1MJNarQYbPc4GADGDv0/qEN29n0UUPkDFmOIY3gl8b\nyRTZUKiskzpIyeL6t71xoiGMdJoAlurXTdiSthtO22cOsfx+Qp7csYgFJIc67GcH\nazFSdZi7AgMBAAECggEAMUvhZLfBteQjQ9784QMOuGe6wjDV1k6pjJCElPYwdPFg\n2mcTGhSMAG6X1Gg66B1Smhuo5kdTfrz4B4vihhJC9gzsEQLaXLf2XE9QkI6wx04Z\nJO2JzrKUAPq6hjKaDvce8ZqfmFa44P2nvf/nk/M1Z8pq4Ln2efwi+KkoN/Wf9R8q\n+hUJiruDOuEWp9ykmyUTi+8Gl1drGEZhT+JhfEoQjVzrTyMIepT3u3M/n3SGdVI6\nvlll4WMXSHR9hei3nnjV5M7mnetB4JPyRkja9JVGDmEOmcInlWJSqiXO0sfJtqwW\nA0wRhvT634gg7pzUlES8UZHA7zArHo3FDSjMPwEF4QKBgQDlj41fbjMSsoJyZzwK\n3ciyNtuuRwOx7D6j0VY0uyCJMCM6VcV/n2oJMTCANA5z/gq2C+5TGWoViGs0ZLi/\nf7Sa6UTCbq13/AeFyZ4gH3TN8+ybkjYHZ9iTbhtIwD1MAphacCUg6StmawlShJbR\nA3E9Dugbb6mjl6dj/u/NErQ9NQKBgQDFp16hrTlzTxHF6t3CzsVLQ6wYSEwGsGbW\n0V7lvR4Ubt50NJ8Q8jhJfzT5s/o2uFPbtc+c6zLisiDW1IXbOxRYY3XpXaWvvpJ1\noY79hpDSEyo6yldkXzfPrI7BFSdX5qfRElu3AHgWEcmlqcPwFbyIMl8Lm9AFh9ey\nQ+RBQNxsLwKBgB/3W3JcgBQsc2nG4l+I/reCWBjunp8aDKb3MY/qNt+jqmQnKXda\nFYPuK5jOpuyUBZ3QD4HW2iTheDw1glx4RggET6TbkKBSoiGJL9G9T6CWRO5s78Uc\nOtZc0MPSsTZybhC56RGqJnb+lK++8tlsJ0qfVsbrR64WIiMUjwP5hMu5AoGAOv3B\nGLACvY+T1mZK2aGs8NG5w2WQi06K4wKKODdBiwesDTLHZt9kPUtiHETDISHSpXiW\nBleMUGypsHStnsj7QYYt4wC4OsO+Iq2dZ72J66kcqX9KpgJlPe5ajPYrT+jfnV7F\nUNErBis46+DHQhi6tEuUYnqWk4//qIzqyy74mrECgYEA4bT/kpbS+E74Y7raEPbh\njL8aeJiU+bueZsozyNgc5KeWcT70xV21DZDq9UVvgIwNCqc/q9P5v02nA0PH/Y2G\nlTAii/I4WOHegArVWU59DHCope2n5KPG1cBk1iCaiY6fJq+QYR2zmAygXvASBrK3\nkP1fRHrNYMxSjhHHInp7L8k=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@fir-todo-auth-3b183.iam.gserviceaccount.com",
  "client_id": "102273664009737030066",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40fir-todo-auth-3b183.iam.gserviceaccount.com",
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