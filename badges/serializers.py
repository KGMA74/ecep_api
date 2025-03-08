from rest_framework import serializers
from .models import Badge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'image', 'created_by', 'is_approved']
        read_only_fields = ['created_by', 'is_approved']  # Les teachers ne peuvent pas approuver eux-mêmes
