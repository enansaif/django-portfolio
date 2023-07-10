"""
Contact Form for Portfolio project
"""
from django import forms

textarea_widget = forms.Textarea(attrs={'rows':'8', 'class': 'form-control',
                                        'style':'resize:none'})
textinput_widget = forms.TextInput(attrs={'class': 'form-control'})

class ContactForm(forms.Form):
    """
    A contact form for users to submit inquiries.

    Fields:
        name (CharField): The name of the user submitting the form.
        email (EmailField): The email address of the user.
        subject (CharField): The subject of the inquiry.
        content (CharField): The content or message of the inquiry.
    """
    name = forms.CharField(max_length=200, label='Name', widget=textinput_widget)
    email = forms.EmailField(label='Email', widget=textinput_widget)
    subject = forms.CharField(label='Subject', widget=textinput_widget)
    content = forms.CharField(label='Content', widget=textarea_widget)
    