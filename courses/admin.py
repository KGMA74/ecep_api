from django.contrib import admin
from .models import Course, CourseProgress, CourseRequest

# Register your models here.
admin.site.register([
    Course,
    CourseRequest,
    CourseProgress
])