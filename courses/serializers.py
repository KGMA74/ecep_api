from rest_framework import serializers
from .models import Course, CourseRequest, CourseProgress

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_by']        

class CourseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'
        
class CourseProgressSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseProgress
        fields = '__all__'
        
