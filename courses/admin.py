from django.contrib import admin
from .models import Course, CourseProgress, Matter

# Register your models here.
admin.site.register([
    Course,
    Matter,
    CourseProgress
])