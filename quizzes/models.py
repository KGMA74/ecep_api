from django.db import models
from courses.models import CourseProgress
from django.db.models.signals import post_save
from django.dispatch import receiver

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    course = models.ForeignKey('courses.Course', related_name='quizzes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def create_quiz(self):
        """Créer un quiz."""
        self.save()

    def delete_quiz(self):
        """Supprimer un quiz."""
        self.delete()

    def grade_quiz(self, student, grade):
        """Attribuer une note à un étudiant pour ce quiz."""
        progress = CourseProgress.objects.filter(course=self.course, student=student).first()
        if progress:
            progress.grade_quiz(self, grade)
  
class Question(models.Model):
    quiz = models.ForeignKey('quizzes.Quiz', related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(help_text="The question text")
    points = models.IntegerField(default=1, help_text="Points assigned to this question")

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey('quizzes.Question', related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, help_text="The text of the answer")
    is_correct = models.BooleanField(default=False, help_text="Indicates whether the answer is correct")

    def __str__(self):
        return self.text
    
class QuizResult(models.Model):
    progress = models.ForeignKey('courses.CourseProgress', related_name='quiz_results', on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', related_name='quiz_results', on_delete=models.CASCADE)
    grade = models.FloatField(null=True, blank=True)  # Note obtenue dans le quiz
    answers = models.ManyToManyField('quizzes.Answer', related_name='quiz_results')
    
    class Meta:
        unique_together = ('progress', 'quiz')

    def __str__(self):
        return f"Result for {self.progress.student} in quiz {self.quiz.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.grade is None and self.answers.exists():
            self.calculate_grade()

    def calculate_grade(self):
        """Calculer la note de l'étudiant pour ce quiz en fonction des réponses correctes."""
        total_points = 0
        total_possible_points = 0
        
        for question in self.quiz.questions.all():
            correct_answers_for_question = question.answers.filter(is_correct=True)
            selected_answers_for_question = self.answers.filter(question=question)
            
            correct_count = correct_answers_for_question.count()
            selected_correct_count = selected_answers_for_question.filter(is_correct=True).count()
            
            total_possible_points += question.points
            
            if selected_correct_count == correct_count and selected_answers_for_question.count() == selected_correct_count:
                total_points += question.points

        if total_possible_points > 0:
            self.grade = (total_points / total_possible_points) * 100
        else:
            self.grade = 0
            
        self.save(update_fields=['grade'])

# Utilisation d'un signal pour calculer la note automatiquement
@receiver(post_save, sender=QuizResult)
def calculate_quiz_result_grade(sender, instance, **kwargs):
    if instance.grade is None and instance.answers.exists():
        instance.calculate_grade()


