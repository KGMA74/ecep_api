from .serializers import ProfileSerializer, StudentSerializer, TeacherSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )

        return response
    
#customisation de la class TokenObtainPairView pour que les tokens passes par les cookies et non les headers donc plus securise
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
        
        #un cookie pour le access token
        response.set_cookie(
            'access',
            access_token,
            max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )
        
        #un cookie pour le refresh token
        response.set_cookie(
            'refresh',
            refresh_token,
            max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )
            
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) :
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            #si le token refresh dans le la list des cookies
            request.data['refresh'] = refresh_token
            
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            print("Access token:", access_token)
            
            #on met a jour le access token
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                path=settings.AUTH_COOKIE_PATH,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token:
            request.data['token'] = access_token
            
        return super().post(request, *args, **kwargs)
    

    
@api_view(['POST'])
def LogoutView(request):
    if request.method == 'POST':
        # Supprimer les tokens en mettant leur valeur des cookies à ''
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.set_cookie(
            'refresh',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN 
        )
        
        response.set_cookie(
            'access',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )

        # Ajouter les tokens à la liste de blackliste

        refresh_token = request.data.get('refresh', None)
        access_token = request.data.get('access', None)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            pass
        
        try:
            token = AccessToken()
            token.ton_bac
        except Exception as e:
            pass

        return response
    
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def createStudent(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)