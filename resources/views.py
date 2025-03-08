from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Student
from .models import Resource, Video, Document, Image, Audio
from .serializers import ResourcePolymorphicSerializer


# Create your views here
# crud 1111



class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ResourcePolymorphicSerializer
    
    @action(detail=False, methods=['get'], url_path='videos')
    def video(self, request):
        videos = Video.objects.all()
        page = self.paginate_queryset(videos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='docouments')
    def document(self, request):
        documents = Document.objects.all()
        page = self.paginate_queryset(documents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='audios')
    def audio(self, request):
        audios = Audio.objects.all()
        page = self.paginate_queryset(audios)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(audios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='images')
    def image(self, request):
        images = Image.objects.all()
        page = self.paginate_queryset(images)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    
# enrolle_student
api_view(['POST'])
def enrolle_student(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        student.courses.add(request.data['course_id'])
        student.save()
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

