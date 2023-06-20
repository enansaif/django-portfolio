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
    link = models.URLField(max_length=150)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.CASCADE)
    edge_case = models.TextField(max_length=100, blank=True, null=True)
    solution = models.TextField(max_length=300)
    option1 = models.TextField(max_length=300, blank=True, null=True)
    option2 = models.TextField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return f"{self.number}. {self.name}"