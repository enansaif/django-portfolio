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
        number (int): The problem ID.
        name (str): The name of the problem.
        link (str): The LeetCode link for the problem.
        topic (Topic): The topic associated with the problem.
        difficulty (Difficulty): The difficulty level of the problem.
        solution (str): The solution description of the problem.
        edge_case (str): The edge case description of the problem (optional).
        option1 (str): The first wrong answer option (optional).
        option2 (str): The second wrong answer option (optional).

    Usage:
        To create a new problem form and render it in a template:
        ```
        form = CreateProblemForm()
        context = {'form': form}
        return render(request, 'template.html', context)
        ```
    """
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
    """
    Form for creating a topic.

    Fields:
        topic (str): The name of the topic.
    """
    topic = forms.CharField(max_length=20, label='Topic Name', widget=textinput_widget)
