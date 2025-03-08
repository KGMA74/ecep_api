from rest_framework import serializers
from .models import Quiz, CourseProgress, QuizResult

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'duration', 'course']

class CourseProgressSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = CourseProgress
        fields = ['student', 'course', 'quizzes']
        
from rest_framework import serializers
from .models import QuizResult, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']

class QuizResultSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizResult
        fields = ['quiz', 'grade', 'answers']

