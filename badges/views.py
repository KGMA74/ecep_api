from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Badge, User
from .serializers import BadgeSerializer

class BadgeViewSet(viewsets.ModelViewSet):
    """
    VueSet pour gérer les badges :
    - Lister tous les badges (seuls les badges approuvés pour les non-admins)
    - Voir un badge spécifique
    - Attribuer un badge à un utilisateur sous certaines conditions
    - Voir les badges d'un utilisateur
    - Proposer un badge (enseignant)
    - Approuver un badge (admin uniquement)
    """
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "name"  # Utilisation de `name` comme identifiant unique

    def get_queryset(self):
        """Les enseignants et étudiants voient seulement les badges approuvés.
        Les enseignants voient aussi les badges qu'ils ont créés, même s'ils ne sont pas encore approuvés.
        """
        user = self.request.user
        if user.role == 'admin':
            return Badge.objects.all()
        if user.role == 'teacher':
            return Badge.objects.filter(Q(is_approved=True) | Q(created_by=user))
        return Badge.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        """Un teacher peut proposer un badge, mais il n'est pas approuvé automatiquement"""
        user = self.request.user
        is_approved = user.role == 'admin'  # Seuls les admins peuvent créer directement un badge approuvé
        serializer.save(created_by=user, is_approved=is_approved)

    @action(detail=False, methods=["get"])
    def list_badges(self, request):
        """Retourne la liste de tous les badges disponibles."""
        badges = self.get_queryset()
        serializer = self.get_serializer(badges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def award_badge(self, request, name=None):
        """Attribue un badge à un utilisateur s'il remplit les conditions."""
        badge = self.get_object()
        user_id = request.data.get("user_id")
        
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)

        if badge.award_badge(user):
            return Response({"message": f"Badge '{badge.name}' awarded to {user.email}"}, status=status.HTTP_200_OK)
        return Response({"error": "User does not meet the requirements for this badge."}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def approve(self, request, name=None):
        """Un admin peut approuver un badge."""
        badge = get_object_or_404(Badge, name=name)

        if request.user.role != 'admin':
            return Response({"error": "Only admins can approve badges"}, status=status.HTTP_403_FORBIDDEN)

        badge.approve()
        return Response({"message": f"Badge '{badge.name}' has been approved"}, status=status.HTTP_200_OK)

class UserBadgeView(APIView):
    """Vue dédiée pour récupérer les badges d’un utilisateur"""
    
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        badges = user.badges.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
