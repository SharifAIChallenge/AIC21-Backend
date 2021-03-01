from django.db import models


class QuestionTitle(models.Model):
    title = models.CharField(max_length=512)


class QuestionWithAnswer(models.Model):
    title = models.ForeignKey(QuestionTitle, related_name='faqs',
                              on_delete=models.CASCADE, null=True)
    question_en = models.CharField(max_length=1024)
    question_fa = models.CharField(max_length=1024)
    answer_en = models.CharField(max_length=1024)
    answer_fa = models.CharField(max_length=1024)
