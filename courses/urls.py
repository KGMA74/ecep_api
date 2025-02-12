from rest_framework.routers import DefaultRouter
from .views import CourseRequestViewSet

router = DefaultRouter()
router.register(r"course-requests", CourseRequestViewSet, basename="course-request")

urlpatterns = router.urls
