from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Student
from .models import Resource
from .serializers import ResourceSerializer


# Create your views here
# crud 1111



class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    
    
# enrolle_student
api_view(['POST'])
def enrolle_student(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        student.courses.add(request.data['course_id'])
        student.save()
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

