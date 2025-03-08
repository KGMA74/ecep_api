from rest_framework.serializers import ModelSerializer
from .models import Course, CourseRequest, CourseProgress

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRequestSerializer(ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'
        
class CourseProgressSerializer(ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = '__all__'
        
