from django.contrib import admin
from .models import User, Student, Parent

# Register your models here.
admin.site.register(
    User,
    list_display=['email', 'nickname', 'role', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at'],
    list_filter=['role', 'is_active', 'is_staff', 'is_superuser'],
    search_fields=['email', 'nickname'],
    ordering=['email']
)

admin.site.register([Student, Parent])