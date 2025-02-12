from rest_framework.serializers import Serializer
from .models import Course

class CourseSerializer(Serializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRequestSerializer(Serializer):
    class Meta:
        model = Course
        fields = '__all__'