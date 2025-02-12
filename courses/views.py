from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework import generics, status, viewsets
from users.models import Teacher
from .models import Course, CourseRequest, CourseProgress
from .serializers import CourseSerializer, CourseRequestSerializer, CourseProgressSerializer

# Create your views here.

# api_view(['POST'])
# def createCourse(request):
#     if request.method == 'POST':
#         user = request.user
#         if isinstance(user, Teacher):
#             serializer = CourseSerializer(data=request.data)
            
#             if serializer.is_valid():
#                 serializer.save() 
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
#             else:
#                 return Response()
#         else:
#             Response("You must be a Teacher!", status=status.HTTP_403_FORBIDDEN)
                   
#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class retrieveCourseView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'
    
    


class ReviewCourseRequestView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, request_id):
        course_request = get_object_or_404(CourseRequest, id=request_id)
        action = request.data.get("action")

        if action == "approve":
            course_request.approve(admin_user=request.user)
            return Response({"message": f"Course approved by {request.user.email}!"})

        elif action == "reject":
            course_request.reject(admin_user=request.user)
            return Response({"message": f"Course rejected by {request.user.email}!"})

        return Response({"error": "Invalid action"}, status=400)
    
    

class CourseRequestViewSet(viewsets.ModelViewSet):
    queryset = CourseRequest.objects.all()
    serializer_class = CourseRequestSerializer

    def get_permissions(self):
        """Définit les permissions pour chaque action."""
        if self.action in ["approve", "reject", "list"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Création d'une demande par un professeur uniquement."""
        user = self.request.user
        if not user.role == "teacher":
            return Response({"error": "Only teachers can create course requests."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(teacher=user, status="pending")

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Un admin valide la demande et crée le cours."""
        course_request = get_object_or_404(CourseRequest, pk=pk, status="pending")
        if not request.user.is_staff:
            return Response({"error": "Only admins can approve requests."}, status=status.HTTP_403_FORBIDDEN)
        
        course = course_request.approve(admin_user=request.user)
        return Response({"message": "Course request approved.", "course": CourseSerializer(course).data})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Un admin refuse la demande."""
        course_request = get_object_or_404(CourseRequest, pk=pk, status="pending")
        if not request.user.is_admin:
            return Response({"error": "Only admins can reject requests."}, status=status.HTTP_403_FORBIDDEN)

        course_request.reject(admin_user=request.user)
        return Response({"message": "Course request rejected."}, status=status.HTTP_200_OK)


class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        """ Récupère la progression d'un utilisateur dans un cours spécifique. """
        course_progress = get_object_or_404(CourseProgress, user=request.user, course_id=course_id)
        serializer = CourseProgressSerializer(course_progress)
        return Response(serializer.data)

    def patch(self, request, course_id):
        """ Met à jour la progression ou la note d'un utilisateur pour un cours. """
        course_progress = get_object_or_404(CourseProgress, user=request.user, course_id=course_id)
        
        # Mise à jour de la progression ou de la note
        progress = request.data.get('progress_percentage')
        grade = request.data.get('grade')

        if progress is not None:
            course_progress.update_progress(progress)
        
        if grade is not None:
            course_progress.add_grade(grade)

        # Sérialiser les nouvelles données
        serializer = CourseProgressSerializer(course_progress)
        return Response(serializer.data, status=status.HTTP_200_OK)