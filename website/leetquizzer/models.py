"""
LeetQuizzer database models
"""
from django.db import models


class Topic(models.Model):
    """
    Model representing a topic.

    Attributes:
        name (str): The name of the topic.
    """
    name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name}"


class Difficulty(models.Model):
    """
    Model representing a difficulty level.

    Attributes:
        name (str): The name of the difficulty level.
    """
    name = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.name}"


class Problem(models.Model):
    """
    Model representing a problem.

    Attributes:
        name (str): The name of the problem.
        number (int): The problem number.
        link (str): The URL link for the problem.
        wrong (bool): Indicates whether the problem is marked as wrong.
        time (datetime): The timestamp for when the problem was last modified.
        topic (Topic): The topic associated with the problem.
        difficulty (Difficulty): The difficulty level of the problem.
        solution (str): The solution description of the problem.
        option1 (str): The first option for the problem (optional).
        option2 (str): The second option for the problem (optional).
        edge_case (str): The edge cases of the problem (optional).
    """
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    link = models.URLField(max_length=150)
    wrong = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.CASCADE)
    solution = models.TextField(max_length=300)
    option1 = models.TextField(max_length=300, blank=True, null=True)
    option2 = models.TextField(max_length=300, blank=True, null=True)
    edge_case = models.TextField(max_length=300, blank=True, null=True)
    def __str__(self):
        return f"{self.number}. {self.name}"
    