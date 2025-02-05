from django.http.request import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    """
        Ici on fait juste une surcharge de la fonction authenticate de JWTAuthentication pour recuperer les tokens( access token) au lieu de les recuperer dans les headers
        pour des raisons de securité_
        
    """
    
    def authenticate(self, request: HttpRequest):
        try:
            header = self.get_header(request)
            
            if header is None:
                #on recuperer le token à partir du  cookie access
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
                print('--------------------', raw_token)
            else:
                raw_token = self.get_raw_token(header)
                
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None
