from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .manager import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    #la definition du champ password n'est pas necessaire car faite par defaut par django
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email
    
    def has_module_perms(self, obj=None):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.nickname}"

# === User Specialization === #
class Teacher(User):
    specialty = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    courses = models.ManyToManyField('courses.Course', related_name="teachers")

    def __str__(self):
        return f"Teacher: {self.nickname}"

class Student(User):
    student_id = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=50)
    courses = models.ManyToManyField('courses.Course', related_name="students")

    def __str__(self):
        return f"Student: {self.nickname} ({self.student_id})"
    
class Parent(User):
    children = models.ManyToManyField(Student, related_name='parents', blank=True)

    def __str__(self):
        return f"Parent: {self.username}"
    
#pour la creation d un profile auto associe un new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)