from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatterViewSet, CourseProgressViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"matters", MatterViewSet, basename="matter")
router.register(r"course-progress", CourseProgressViewSet, basename="course-progress")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path('', include(router.urls))
]
