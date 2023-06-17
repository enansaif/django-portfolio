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
    #topic = models.ForeignKey('Topic', null=False, on_delete=models.CASCADE)
    #difficulty = models.ForeignKey('Difficulty', null=True, on_delete=models.SET_NULL)
    solution = models.CharField(max_length=500)
    edge_case = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.number}. {self.name}"