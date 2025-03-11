from .serializers import (
    ProfileSerializer, TeacherSerializer, StudentSerializer, ParentSerializer,
    EnrollCourseSerializer, AddChildSerializer, XPTransactionSerializer
)
from .models import Profile, Teacher, Student, Parent, Student
from django.conf import settings 
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from courses.serializers import CourseSerializer
from courses.models import Course
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, action, permission_classes
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )

        return response
    
#customisation de la class TokenObtainPairView pour que les tokens passes par les cookies et non les headers donc plus securise
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
        
        #un cookie pour le access token
        response.set_cookie(
            'access',
            access_token,
            max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )
        
        #un cookie pour le refresh token
        response.set_cookie(
            'refresh',
            refresh_token,
            max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )
            
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) :
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            #si le token refresh dans le la list des cookies
            request.data['refresh'] = refresh_token
            
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            print("Access token:", access_token)
            
            #on met a jour le access token
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                path=settings.AUTH_COOKIE_PATH,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token:
            print(access_token, '-----')
            mutable_data = request.data.copy()
            mutable_data['token'] = access_token
            request._full_data = mutable_data
            
        return super().post(request, *args, **kwargs)
    
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import User, Student, Teacher, Parent, Level
from .serializers import UserSerializer

class CustomUserViewSet(UserViewSet):

    def perform_create(self, serializer, *args, **kwargs):
        
        
        # serializer = self.get_serializer(data=request.data)
        super().perform_create(serializer)
        user = serializer.instance 
        # if serializer.is_valid():
        #     user = serializer.save()
            

        # Création du profil en fonction du rôle
        role = user.role
        print("mmmmmmmmmmmmmmmmmrole=", role)
        if role == "student":
            # level_id = request.data.get("level")
            # level = Level.objects.get(id=level_id) if level_id else None
            Student.objects.create(user=user)
        elif role == "teacher":
            print("999999999999999999999999999999999")
            specialty = self.request.data.get("specialty", "")
            degree = self.request.data.get("degree", "")
            Teacher.objects.create(user=user, specialty=specialty, degree=degree)
        elif role == "parent":
            Parent.objects.create(user=user)

        # Réponse de succès
        return Response({
            "message": "User registered successfully",
            "user": {
                "email": user.email,
                "firstname": user.firstname,
                "role": role
            }
        }, status=status.HTTP_201_CREATED)

    # En cas d'erreurs de validation dans le sérialiseur
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    if request.method == 'POST':
        # Supprimer les tokens en mettant leur valeur des cookies à ''
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.set_cookie(
            'refresh',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN 
        )
        
        response.set_cookie(
            'access',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )

        # Ajouter les tokens à la liste de blackliste

        refresh_token = request.data.get('refresh', None)
        access_token = request.data.get('access', None)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            pass
        
        try:
            token = AccessToken(access_token)
            
        except Exception as e:
            pass
        
        return response
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def createStudent(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Inscrire un étudiant à un cours."""
        student = self.get_object()
        serializer = EnrollCourseSerializer(data=request.data)
        if serializer.is_valid():
            course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
            student.enroll_in_course(course)
            return Response({'message': 'Student enrolled successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def enrolled_courses(self, request, pk=None):
        """Liste des cours auxquels l'étudiant est inscrit."""
        student = self.get_object()
        courses = student.courses_enrolled.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def drop(self, request, pk=None):
        """Désinscrire un étudiant d’un cours."""
        student = self.get_object()
        serializer = EnrollCourseSerializer(data=request.data)
        if serializer.is_valid():
            course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
            student.courses.remove(course)
            return Response({'message': 'Student dropped from course'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["post"])
    def add_xp(self, request, pk=None):
        """Permet d'ajouter des XP à un élève et de mettre à jour son niveau."""
        student = self.get_object()
        points = request.data.get("points")

        if not points:
            return Response({"error": "Points are required"}, status=status.HTTP_400_BAD_REQUEST)

        student.add_xp(points)
        return Response({"message": f"{points} XP added to {student.user.fullname}. Current level: {student.level.name}"}, status=status.HTTP_200_OK)

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    @action(detail=True, methods=['post'])
    def add_child(self, request, pk=None):
        """Ajouter un enfant à un parent."""
        parent = self.get_object()
        serializer = AddChildSerializer(data=request.data)
        if serializer.is_valid():
            student = get_object_or_404(Student, id=serializer.validated_data['student_id'])
            parent.children.add(student)
            return Response({'message': 'Child added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_child(self, request, pk=None):
        """Supprimer un enfant d’un parent."""
        parent = self.get_object()
        serializer = AddChildSerializer(data=request.data)
        if serializer.is_valid():
            student = get_object_or_404(Student, id=serializer.validated_data['student_id'])
            parent.children.remove(student)
            return Response({'message': 'Child removed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserXPViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def xp(self, request, pk=None):
        """Retourne l'XP total d'un utilisateur donné."""
        student = get_object_or_404(Student, pk=pk)
        return Response({"total_xp": student.xp}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def xp_history(self, request, pk=None):
        """Retourne l'historique des transactions de XP d'un utilisateur."""
        student = get_object_or_404(Student, pk=pk)
        transactions = student.xp_transactions.all()
        serializer = XPTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudentLevelViewSet(viewsets.ViewSet):
    queryset = Student.objects.all()

    @action(detail=True, methods=["get"])
    def level(self, request, pk=None):
        """Retourne le niveau actuel de l'élève."""
        student = self.get_object()
        return Response({"level": student.level}, status=status.HTTP_200_OK)

