from django.db import models
from courses.models import Course, CourseProgress

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

    def __str__(self):
        return f"Result for {self.progress.student} in quiz {self.quiz.title}"

    def calculate_grade(self):
        """Calculer la note de l'étudiant pour ce quiz en fonction des réponses correctes."""
        correct_answers = self.answers.filter(is_correct=True)
        correct_answer_count = correct_answers.count()

        # Récupérer les réponses correctes attendues pour chaque question
        total_points = 0
        for question in self.quiz.questions.all():
            correct_answers_for_question = question.answers.filter(is_correct=True)
            selected_answers_for_question = self.answers.filter(question=question)

            # Comparer les réponses de l'étudiant avec celles qui sont correctes
            correct_count = correct_answers_for_question.count()
            selected_correct_count = selected_answers_for_question.filter(is_correct=True).count()

            # Si toutes les bonnes réponses sont sélectionnées et rien d'incorrect n'est sélectionné
            if selected_correct_count == correct_count and selected_answers_for_question.count() == correct_answers_for_question.count():
                total_points += question.points  # Ajouter les points de la question

        # Calculer la note sur 100
        total_questions = self.quiz.questions.count()
        self.grade = (total_points / (total_questions * 1.0)) * 100
        self.save()



