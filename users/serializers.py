from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Profile, Student, Teacher, Parent, XPTransaction

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('role', 'profile')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['profile'] = ProfileSerializer(instance.profile, many=False).data
        
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data

class EnrollCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

class AddChildSerializer(serializers.Serializer):
    pass
    student_id = serializers.IntegerField()
    


class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = ['user', 'xp_points', 'reason', 'created_at']
        read_only_fields = ['user', 'created_at']


