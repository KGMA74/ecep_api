from django.db import models
from django.utils import timezone
from core.models import BaseModel

class Course(BaseModel):
    MATTER_CHOICES = [
        ('Histoire', 'histoire'),
        ('Geographie', 'geographie'),
        ('Francais', 'francais'),
        ('Mathematique', 'mathematique')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    syllabus = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(default=1)
    matter = models.CharField(choices=MATTER_CHOICES, default='francais', max_length=50)
    min_level_required = models.IntegerField(default=1)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")
    students = models.ManyToManyField("users.Student", related_name="courses_enrolled", blank=True)
    created_from_request = models.OneToOneField(
        "CourseRequest", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_course"
    )
    
    def __str__(self):
        return self.title

class CourseRequest(models.Model):
    MATTER_CHOICES = [
        ('Histoire', 'histoire'),
        ('Geographie', 'geographie'),
        ('Francais', 'francais'),
        ('Mathematique', 'mathematique')
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    requested_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="course_requests")
    mattter = models.CharField(choices=MATTER_CHOICES, default='francais', max_length=50)
    syllabus = models.FileField(upload_to='syllabus/')
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(default=1)
    min_level_required = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")    
    reviewed_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_courses")
    progessPercentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def approve(self, admin_user):
        """Approuve la demande et crée le cours"""
        course = Course.objects.create(
            title=self.title,
            description=self.description,
            syllabus=self.syllabus,
            start_date=self.start_date,
            end_date=self.end_date,
            credits=self.credits,
            created_by = self.requested_by,
            min_level_required=self.min_level_required
        )
        self.status = "approved"
        self.reviewed_by = admin_user
        self.save() #si on veut garder les traces
        # self.delete() #si on veut supprimer la demande
        return course

    def reject(self, admin_user):
        """Rejette la demande"""
        self.status = "rejected"
        self.reviewed_by = admin_user
        self.save()
        # self.delete()

    def __str__(self):
        return self.title
    
    '''
    TODO: rechercher comment ajouter la gestions des statistique pour l'utilisateur admin
    '''
    

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
