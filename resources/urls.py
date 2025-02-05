from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')

# GET /resources/ → Liste toutes les ressources.
# POST /resources/ → Crée une nouvelle ressource.
# GET /resources/<id>/ → Récupère une ressource spécifique.
# PUT /resources/<id>/ ou PATCH /resources/<id>/ → Met à jour la ressource.
# DELETE /resources/<id>/ → Supprime la ressource.

urlpatterns = [
    path('', include(router.urls))
]
