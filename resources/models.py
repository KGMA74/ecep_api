from django.db import models
from polymorphic.models import PolymorphicModel

# -------- resources
class Resource(PolymorphicModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey("courses.Course", related_name='resources', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Video(Resource):
    duration = models.DurationField()
    file = models.FileField(upload_to='resources/videos/')

class Image(Resource):
    resolution = models.CharField(max_length=50)
    file = models.ImageField(upload_to='resources/images/')
    
class Audio(Resource):
    file = models.FileField(upload_to='resources/audios/')
    
class Document(Resource):
    file = models.FileField(upload_to='resources/documents/')