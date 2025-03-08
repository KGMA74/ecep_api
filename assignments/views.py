from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Assignment
from users.models import Course, Teacher, Student
from .serializers import AssignmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Lors de la création d'une tâche, associer le professeur à la tâche"""
        user = self.request.user
        teacher = get_object_or_404(Teacher, user=user)  # On suppose que le User est lié à un Teacher
        serializer.save(created_by=teacher)  # Associer le professeur qui crée la tâche

    @action(detail=False, methods=["get"])
    def list_assignments(self, request):
        """Retourne la liste de toutes les tâches"""
        assignments = self.get_queryset()
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def grade_assignment(self, request, pk=None):
        """Attribue une note à une tâche"""
        assignment = self.get_object()
        grade = request.data.get("grade")
        
        if grade is None:
            return Response({"error": "Grade is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        assignment.grade_assignment(grade)
        return Response({"message": f"Grade {grade} assigned to assignment '{assignment.title}'."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["delete"])
    def delete_assignment(self, request, pk=None):
        """Supprime une tâche"""
        assignment = self.get_object()
        assignment.delete_assignment()
        return Response({"message": f"Assignment '{assignment.title}' deleted."}, status=status.HTTP_204_NO_CONTENT)
