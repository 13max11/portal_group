from django.db import models
from auth_sys import models as auth_models

# Create your models here.
class Grade(models.Model):
    user = models.ManyToManyField(auth_models.CustomUser, related_name="Grade")
    grade = models.IntegerField()
    lesson_date = models.DateTimeField()# Дата уроку за яку вчитель ставить оцінку
    creation_date = models.DateField(auto_now_add=True)# Дата дня в який читель поставив оцінку