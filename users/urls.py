from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LogoutView,
    ProfileViewSet, TeacherViewSet, StudentViewSet, ParentViewSet
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'parents', ParentViewSet)


urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView),
    path('', include('djoser.urls')),
    path('', include(router.urls))
]
