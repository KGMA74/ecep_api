from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseRequestViewSet, CourseProgressViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"course-requests", CourseRequestViewSet, basename="course-request")
router.register(r"course-progress", CourseProgressViewSet, basename="course-progress")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path('', include(router.urls))
]
