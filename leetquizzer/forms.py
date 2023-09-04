"""
Forms for LeetQuizzer database insertion
"""
from django import forms
from leetquizzer.models import Topic, Difficulty

textarea_widget = forms.Textarea(attrs={'rows':'2', 'class': 'form-control', 'style':'resize:none'})
textinput_widget = forms.TextInput(attrs={'class': 'form-control'})
link_widget = forms.TextInput(attrs={'class': 'form-control',
                             'placeholder': 'https://leetcode.com/problems/<problem-title>/'})
choice_widget=forms.Select(attrs={'class':'form-control'})
topic = Topic.objects.all()
difficulty = Difficulty.objects.all()


class CreateProblemForm(forms.Form):
    """
    Form for creating a problem.

    Fields:
        link (str): The LeetCode link for the problem.
        topic (Topic): The topic associated with the problem.
        solution (str): The best solution of the problem.
        edge_case (str): The edge cases of the problem (optional).
        option1 (str): The brute force solution (optional).
        option2 (str): Any other unoptimized solution (optional).
    """
    link = forms.URLField(max_length=150, label='LeetCode Link*', widget=link_widget)
    topic = forms.ModelChoiceField(queryset=topic, label='Topic*', widget=choice_widget)
    solution = forms.CharField(max_length=300, label='Best Solution*', widget=textarea_widget)
    option1 = forms.CharField(max_length=300, required=False, label='Brute Force',
                              widget=textarea_widget)
    option2 = forms.CharField(max_length=300, required=False, label='Unoptimized',
                              widget=textarea_widget)
    edge_case = forms.CharField(max_length=300, required=False, label='Edge Cases',
                                widget=textarea_widget)


class UpdateProblemForm(forms.Form):
    """
    Form for creating a problem.
    """
    topic = forms.ModelChoiceField(queryset=topic, label='Topic*', widget=choice_widget)
    solution = forms.CharField(max_length=300, label='Best Solution*', widget=textarea_widget)
    option1 = forms.CharField(max_length=300, required=False, label='Brute Force',
                              widget=textarea_widget)
    option2 = forms.CharField(max_length=300, required=False, label='Unoptimized',
                              widget=textarea_widget)
    edge_case = forms.CharField(max_length=300, required=False, label='Edge Cases',
                                widget=textarea_widget)


class CreateTopicForm(forms.Form):
    """
    Form for creating a topic.

    Fields:
        topic (str): The name of the topic.
    """
    topic = forms.CharField(max_length=20, label='Topic Name', widget=textinput_widget)
