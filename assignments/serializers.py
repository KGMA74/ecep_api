from .models import Assignment
from rest_framework.serializers import ModelSerializer

class AssignmentSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"