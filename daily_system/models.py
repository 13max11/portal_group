from django.db import models


class Lesson(models.Model):
    STATUS_CHOICES = [
        ('missing', 'Відсутній'),
        ('present', 'Присутній'),
    ]
    date = models.DateTimeField()
    theme = models.CharField(max_length=80)
    presence = models.CharField(max_length=27, 
                choices=STATUS_CHOICES, default='missing')#відсутність чи присутністьь учня на уроці

    def __str__(self):
        return f'{self.theme} - {self.date}'
    
    
class Homework(models.Model):
    STATUS_CHOICES = [
        ('done', "Зроблено"),
        ('in_progress', "Робиться"),
        ('to_do', "Треба зробити"),
    ]

    grade = models.IntegerField()
    homework = models.CharField(max_length=180)
    status = models.CharField(max_length=27, 
                    choices=STATUS_CHOICES, default='to_do')#виконання домашки
    file = models.FileField(upload_to="comments_media/", blank=True, null=True) #файл виконаного проекта

    

