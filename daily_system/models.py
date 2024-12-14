from django.db import models


class Lesson(models.Model):
    date = models.DateTimeField()
    theme = models.CharField(max_length=80)
    presence = models.CharField(max_length=20, choices=[
        ('present', "Present"),
        ('missing', "Missing"),
    ]) #відсутність чи присутністьь учня на уроці

    def __str__(self):
        return f'{self.theme} - {self.date}'
    
    
class Homework(models.Model):
    grade = models.IntegerField()
    homework = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('done', "Done"),
        ('in_progress', "In progress"),
        ('to_do', "To do"),
    ]) #виконана чи невиконана домашка
    file = models.FileField(upload_to="comments_media/", blank=True, null=True) #файл виконаного проекта

    def __str__(self):
        return self.homework
