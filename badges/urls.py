from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeView

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename="badge")

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/badges/', UserBadgeView.as_view(), name='user-badges')
]
