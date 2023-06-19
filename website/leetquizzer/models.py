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
    topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL)
    difficulty = models.ForeignKey('Difficulty', null=True, on_delete=models.SET_NULL)
    edge_case = models.TextField(null=True)
    solution = models.TextField(null=True)
    option1 = models.TextField(null=True)
    option2 = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.number}. {self.name}"