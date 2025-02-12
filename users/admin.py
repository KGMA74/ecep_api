from django.contrib import admin
from .models import User, Student

# Register your models here.
admin.site.register(
    User,
    list_display=['email', 'nickname', 'role', 'is_active', 'is_staff', 'is_superuser'],
    list_filter=['role', 'is_active', 'is_staff', 'is_superuser'],
    search_fields=['email', 'nickname'],
    ordering=['email']
)