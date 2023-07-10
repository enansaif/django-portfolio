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
    """
    Form for creating a problem.

    Fields:
        link (str): The LeetCode link for the problem.
        topic (Topic): The topic associated with the problem.
        solution (str): The solution description of the problem.
        edge_case (str): The edge case description of the problem (optional).
        option1 (str): The first wrong answer option (optional).
        option2 (str): The second wrong answer option (optional).
    """
    link = forms.URLField(max_length=150, label='LeetCode Link*', widget=textinput_widget)
    topic = forms.ModelChoiceField(queryset=topic, label='Topic*', widget=choice_widget)
    solution = forms.CharField(max_length=300, label='Solution*', widget=textarea_widget)
    edge_case = forms.CharField(max_length=100, required=False, label='Edge Case',
                                widget=textinput_widget)
    option1 = forms.CharField(max_length=300, required=False, label='Wrong Answer',
                              widget=textarea_widget)
    option2 = forms.CharField(max_length=300, required=False, label='Wrong Answer',
                              widget=textarea_widget)


class CreateTopicForm(forms.Form):
    """
    Form for creating a topic.

    Fields:
        topic (str): The name of the topic.
    """
    topic = forms.CharField(max_length=20, label='Topic Name', widget=textinput_widget)
