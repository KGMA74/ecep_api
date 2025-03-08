from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Resource, Video, Image, Audio, Document

   
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        
        
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        
        
class ResourcePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Resource: ResourceSerializer,
        Video: VideoSerializer,
        Document: DocumentSerializer,
        Image: ImageSerializer,
        Audio: AudioSerializer
    }