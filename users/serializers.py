from rest_framework.serializers import Serializer
from .models import Profile, Student, Teacher, Parent

class ProfileSerializer(Serializer):
    class Meta:
        model = Profile
        fields = '__all__'

class StudentSerializer(Serializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class TeacherSerializer(Serializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ParentSerializer(Serializer):
    class Meta:
        model = Parent
        fields = '__all__'
        
        

