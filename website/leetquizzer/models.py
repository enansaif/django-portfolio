from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Difficulty(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

    
class Problem(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    link = models.URLField(max_length=150, null=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL)
    difficulty = models.ForeignKey('Difficulty', null=True, on_delete=models.SET_NULL)
    edge_case = models.TextField(max_length=100, null=True)
    solution = models.TextField(max_length=300, null=True)
    option1 = models.TextField(max_length=300, null=True)
    option2 = models.TextField(max_length=300, null=True)
    
    def __str__(self):
        return f"{self.number}. {self.name}"