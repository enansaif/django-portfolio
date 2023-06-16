from django.forms import ModelForm
from leetquizzer.models import Problem


class AddProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'