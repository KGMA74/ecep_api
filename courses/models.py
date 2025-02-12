from django.db import models
from users.models import BaseModel

class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    syllabus = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField()
    min_level_required = models.CharField(max_length=50)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")
    created_from_request = models.OneToOneField(
        "CourseRequest", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_course"
    )
    
    def __str__(self):
        return self.title

class CourseRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    requested_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="course_requests")

    syllabus = models.FileField(upload_to='syllabus/')
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(default=1)
    min_level_required = models.CharField(max_length=50, default='CM2')
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
        return self.names