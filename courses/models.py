from django.db import models
from django.utils import timezone
from core.models import BaseModel

class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    syllabus = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(default=1)
    matter = models.ForeignKey("Matter", on_delete=models.CASCADE, related_name="courses", default="Mathématiques")
    min_level_required = models.IntegerField(default=1)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")
    students = models.ManyToManyField("users.Student", related_name="courses_enrolled", blank=True)

    def __str__(self):
        return self.title

class Matter(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class CourseProgress(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(default=timezone.now) 
    grade = models.FloatField(default=0.0)  
    quizzes = models.ManyToManyField('quizzes.Quiz', through='quizzes.QuizResult')
    completion_status = models.BooleanField(default=False)  
    
    class Meta:
        unique_together = ('student', 'course')
        
    def update_progress(self, new_progress: int):
        """Met à jour le pourcentage de progression et ajuste le statut de complétion."""
        self.progress_percentage = new_progress
        self.last_accessed = timezone.now()  # Mettre à jour la dernière date d'accès
        self.update_completion_status()
        self.save()

    def add_grade(self, new_grade: float):
        """Ajoute un grade et met à jour le statut de complétion en fonction du score."""
        self.grade = new_grade
        self.update_completion_status()
        self.save()

    def update_completion_status(self):
        """Met à jour le statut de complétion du cours en fonction du pourcentage de progression."""
        if self.progress_percentage == 100:  # Seuil de complétion, par exemple 80%
            self.completion_status = True
        else:
            self.completion_status = False
