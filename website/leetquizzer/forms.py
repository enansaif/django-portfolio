"""
Forms for LeetQuizzer database insertion
"""
from django import forms
from leetquizzer.models import Topic, Difficulty

textarea_widget = forms.Textarea(attrs={'rows':'2', 'class': 'form-control', 'style':'resize:none'})
textinput_widget = forms.TextInput(attrs={'class': 'form-control'})
choice_widget=forms.Select(attrs={'class':'form-control'})
topic = Topic.objects.all()
difficulty = Difficulty.objects.all()


class CreateProblemForm(forms.Form):
    number = forms.IntegerField(label='Problem Id*', widget=textinput_widget)
    name = forms.CharField(max_length=100, label='Problem Name*', widget=textinput_widget)
    link = forms.URLField(max_length=150, label='LeetCode Link*', widget=textinput_widget)
    topic = forms.ModelChoiceField(queryset=topic, label='Topic*', widget=choice_widget)
    difficulty = forms.ModelChoiceField(queryset=difficulty, label='Difficulty*',
                                        widget=choice_widget)
    solution = forms.CharField(max_length=300, label='Solution*', widget=textarea_widget)
    edge_case = forms.CharField(max_length=100, required=False, label='Edge Case',
                                widget=textinput_widget)
    option1 = forms.CharField(max_length=300, required=False, label='Wrong Answer',
                              widget=textarea_widget)
    option2 = forms.CharField(max_length=300, required=False, label='Wrong Answer',
                              widget=textarea_widget)


class CreateTopicForm(forms.Form):
    topic = forms.CharField(max_length=20, label='Topic Name', widget=textinput_widget)
