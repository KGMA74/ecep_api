from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    grade = models.FloatField(null=True, blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="assignments")
    students = models.ManyToManyField('users.Student', related_name="assignments")
    created_by = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name="assignments", null=True, blank=True)
    
    def __str__(self):
        return self.title

    def create_assignment(self, title, description, due_date, course, teacher):
        """Méthode pour créer une nouvelle tâche avec un professeur."""
        assignment = Assignment.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            course=course,
            created_by=teacher
        )
        return assignment

    def delete_assignment(self):
        """Méthode pour supprimer une tâche."""
        self.delete()

    def grade_assignment(self, student, grade):
        """Attribuer des notes et des XP à un étudiant après soumission."""
        if grade >= 50:
            xp_points = 50  # Exemple d'attribution de XP pour une bonne note
            student.user.add_xp(xp_points, reason=f"Graded assignment '{self.title}'")
        else:
            xp_points = 20  # Moins de points pour une note faible
            student.user.add_xp(xp_points, reason=f"Graded assignment '{self.title}' with a low score")


