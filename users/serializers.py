from rest_framework import serializers
from .models import Profile, Student, Teacher, Parent

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class EnrollCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

class AddChildSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()


