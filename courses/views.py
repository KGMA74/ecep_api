from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action
from rest_framework import generics, status, viewsets
from users.models import Student, Teacher
from .models import Course, Matter, CourseProgress
from .serializers import CourseSerializer, MatterSerializer, CourseProgressSerializer
from users.serializers import StudentSerializer

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
    
    @action(detail=False, methods=['GET'])
    def user_courses(self, request):
        """Get courses for a specific user or the authenticated user"""
        user_id = request.query_params.get('user_id')

        if user_id and request.user.role in ("admin", "teacher"):
            # Admin can retrieve courses for any user
            queryset = Course.objects.filter(created_by_id=user_id)
        else:
            # Regular users can only view their own courses
            queryset = Course.objects.filter(created_by=request.user)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def enrolled_students(self, request, pk=None):
        """Get all students enrolled in a specific course"""
        course = self.get_object()
        students = Student.objects.filter(courses_enrolled=course)
        
        # Pass the request context to the serializer
        serializer = StudentSerializer(students, many=True, context={'request': request})
        return Response(serializer.data)

    

class MatterViewSet(viewsets.ModelViewSet):
    queryset = Matter.objects.all()
    serializer_class = MatterSerializer
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['GET'])
    def courses(self, request):
        """Get all courses related to a specific matter"""
        matter = self.get_object()
        courses = Course.objects.filter(matter=matter)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)    


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CourseProgress.objects.all()
    
    def retrieve(self, request, pk=None):
        """Get progress for a specific course"""
        course_progress = get_object_or_404(CourseProgress, student=request.user.student, course_id=pk)
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


