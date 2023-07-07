"""
leetQuizzer admin module.
"""
from django.contrib import admin
from .models import Problem, Topic

admin.site.register(Problem)
admin.site.register(Topic)
