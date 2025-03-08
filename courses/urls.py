from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseRequestViewSet, CourseProgressView, CourseViewSet

router = DefaultRouter()
router.register(r"course-requests", CourseRequestViewSet, basename="course-request")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path('course-progress/<int:course_id>/', CourseProgressView.as_view(), name='course-progress'),
    path('', include(router.urls))
]
