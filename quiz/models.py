from django.db import models
import random
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    description = models.CharField(max_length=1000)
    number_of_questions = models.IntegerField()
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    time = models.IntegerField(help_text="Durations of the quiz in minutes", default=1)
    
    
    def __str__(self):
        return f"Quiz '{self.title}' on the topic: {self.topic}"
    
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    
    class Meta:
        verbose_name_plural = "Quizzes"
        

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        answers = list(self.answer_set.all())
        random.shuffle(answers)
        return answers


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.score)