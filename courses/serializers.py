from rest_framework.serializers import Serializer
from .models import Course, CourseRequest, CourseProgress

class CourseSerializer(Serializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRequestSerializer(Serializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'
        
class CourseProgressSerializer(Serializer):
    class Meta:
        model = CourseProgress
        fields = '__all__'