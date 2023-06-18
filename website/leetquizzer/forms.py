from django import forms
from leetquizzer.models import Problem, Topic, Difficulty

textarea_widget = forms.Textarea(attrs={'rows':'3', 'class': 'form-control', 'style':'resize:none'})
textinput_widget = forms.TextInput(attrs={'class': 'form-control'})
choice_widget=forms.Select(attrs={'class':'form-control'})
topic = Topic.objects.all()
difficulty = Difficulty.objects.all()

class AddProblemForm(forms.Form):
    number = forms.IntegerField(label='Problem No.', widget=textinput_widget)
    name = forms.CharField(max_length=100, label='Problem Name', widget=textinput_widget)
    topic = forms.ModelChoiceField(queryset=topic, label='Topic', widget=choice_widget)
    difficulty = forms.ModelChoiceField(queryset=difficulty, label='Difficulty', widget=choice_widget)
    edge_case = forms.CharField(label='Edge Case', widget=textinput_widget)
    solution = forms.CharField(label='Solution', widget=textarea_widget)
    option1 = forms.CharField(label='Wrong 1', widget=textarea_widget)
    option2 = forms.CharField(label='Wrong 2', widget=textarea_widget)

class AddTopicForm(forms.Form):
    topic = forms.CharField(max_length=20, label='Topic Name', widget=textinput_widget)

class AddDifficultyForm(forms.Form):
    difficulty = forms.CharField(max_length=10, label='Difficulty', widget=textinput_widget)
