from django.db import models
from users.models import Student

# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=100, primary_key=True),
    description = models.TextField()
    images = models.ImageField(upload_to='badges/', blank=True, null=True)
    students = models.ManyToManyField('users.Student', related_name='badges', blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="badges_created")
    is_approved = models.BooleanField(default=False) 
    conditions = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def check_conditions(self, user):
        """Vérifie si un utilisateur remplit les conditions pour obtenir ce badge."""
        conditions = self.conditions

        if conditions.get("min_posts") and user.posts.count() < conditions["min_posts"]:
            return False
        if conditions.get("min_reputation") and user.reputation < conditions["min_reputation"]:
            return False
        if conditions.get("has_verified_email") and not user.email_verified:
            return False
        
        return True

    
    def approve(self):
        self.is_approved = True
        self.save()

    def award_badge(self, student):
        if self.is_approved and isinstance(student, Student):
            self.students.add(student)
            return True
        return False

class XPRewardSystem:
    @staticmethod
    def check_rewards(user):
        """Vérifie si un utilisateur mérite un badge ou une récompense en fonction de son XP"""
        if isinstance(user, Student) and user.xp >= 1000:
            badge = Badge.objects.filter(name="Master Learner").first()
            if badge:
                user.badges.add(badge)
                print(f"{user.username} has earned the 'Master Learner' badge!")
