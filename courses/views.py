from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action
from rest_framework import generics, status, viewsets
from users.models import Student, Teacher
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

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=self.request.user)
    
    


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


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CourseProgress.objects.all()
    
    def retrieve(self, request, pk=None):
        """Get progress for a specific course"""
        course_progress = get_object_or_404(CourseProgress, student=request.user, course_id=pk)
        serializer = self.get_serializer(course_progress)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def user_progress(self, request):
        print("**********************************************0")
        """Get all course progress for authenticated student or specific student"""
        student_id = request.query_params.get('student_id')
        print("**********************************************1")
        
        if student_id and (request.user.role in ("admin", "teacher") or request.user.role == "parent" and request.user.parent.children.filter(pk=student_id).exists()):
            queryset = CourseProgress.objects.filter(student_id=student_id)
            print("**********************************************2")
        else:
            # Regular students can only view their own progress
            queryset = CourseProgress.objects.filter(student__user=request.user)
            print("**********************************************3")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        """Update progress or grade for a course"""
        course_progress = get_object_or_404(CourseProgress, student=request.user, course_id=pk)
        
        progress = request.data.get('progress_percentage')
        grade = request.data.get('grade')

        if progress is not None:
            course_progress.update_progress(progress)
        
        if grade is not None:
            course_progress.add_grade(grade)

        serializer = self.get_serializer(course_progress)
        return Response(serializer.data)
    
api_view(['POST'])
def enrolle_student(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        student.courses.add(request.data['course_id'])
        student.save()
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


