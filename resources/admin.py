from django.contrib import admin
from .models import Resource, Video, Document

# Register your models here.
admin.site.register([
    Resource,
    Video,
    Document
])
