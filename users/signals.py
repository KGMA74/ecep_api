from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile, User, Parent, Student, Teacher

#pour la creation d un profile auto associe un new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        role_mapping = {
                    'teacher': Teacher,
                    'student': Student,
                    'parent': Parent
                }
        
        ModelClass = role_mapping.get(instance.role)
        
        if ModelClass:
            ModelClass.objects.get_or_create(user=instance)