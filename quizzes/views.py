from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from users.models import Student
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, CourseProgress, QuizResult, Answer
from .serializers import QuizSerializer, CourseProgressSerializer, QuizResultSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def create_quiz(self, request):
        """Créer un nouveau quiz."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_quiz(self, request, pk=None):
        """Supprimer un quiz."""
        quiz = self.get_object()
        quiz.delete()
        return Response({"message": f"Quiz '{quiz.title}' deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def grade_quiz(self, request, pk=None):
        """Attribuer une note à un quiz pour un étudiant."""
        quiz = self.get_object()
        student_id = request.data.get("student_id")
        grade = request.data.get("grade")

        if not student_id or grade is None:
            return Response({"error": "Student ID and grade are required"}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, pk=student_id)
        progress = student.course_progress.filter(course=quiz.course).first()

        if not progress:
            return Response({"error": "No course progress found for this student"}, status=status.HTTP_400_BAD_REQUEST)

        progress.grade_quiz(quiz, grade)
        return Response({"message": f"Grade {grade} assigned to {student.user.nickname} for quiz '{quiz.title}'"}, status=status.HTTP_200_OK)
    

class QuizResultViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer

    @action(detail=True, methods=["post"], url_path="submit-answers")
    def submit_answers(self, request, pk=None):
        """Soumettre les réponses de l'étudiant pour un quiz."""
        quiz_id = request.data.get("quiz_id")
        student_id = request.data.get("student_id")
        answers_ids = request.data.get("answers_ids")  # Liste des IDs des réponses données

        if not quiz_id or not student_id or not answers_ids:
            return Response({"error": "Quiz ID, Student ID, and answers are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer l'étudiant et le quiz
        student = get_object_or_404(Student, pk=student_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        # Créer ou récupérer le progrès de l'étudiant dans ce quiz
        progress = student.course_progress.filter(course=quiz.course).first()

        if not progress:
            return Response({"error": "No course progress found for this student"}, status=status.HTTP_400_BAD_REQUEST)

        # Créer le résultat du quiz
        quiz_result = QuizResult.objects.create(progress=progress, quiz=quiz)

        # Ajouter les réponses données par l'étudiant
        answers = Answer.objects.filter(id__in=answers_ids)
        quiz_result.answers.set(answers)

        # Calculer la note
        quiz_result.calculate_grade()

        return Response({"message": f"Quiz result saved for {student.user.nickname}"}, status=status.HTTP_201_CREATED)
    
class CourseProgressViewSet(viewsets.ModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer

    @action(detail=True, methods=["get"])
    def quiz_results(self, request, pk=None):
        """Retourner les résultats de quiz pour un étudiant dans un cours spécifique."""
        progress = self.get_object()
        quiz_results = progress.quiz_results.all()
        serializer = QuizResultSerializer(quiz_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
