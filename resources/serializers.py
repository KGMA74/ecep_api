from rest_framework import serializers
from drf_polymorphic.serializers import PolymorphicSerializer
from .models import Resource, Video, Image, Audio

        
class VideoSerializer(serializers.Serializer):
    class Meta:
        model = Video
        fields = '__all__'
        
        
class AudioSerializer(serializers.Serializer):
    class Meta:
        model = Audio
        fields = '__all__'
        
        
class ResourceSerializer(PolymorphicSerializer):
    model_serializer_maping = {
        Video: VideoSerializer,
        Audio: AudioSerializer
    }
        