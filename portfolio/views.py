"""
Serves all templates related to the portfolio application.
"""
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from website.settings import EMAIL_HOST_USER
from .forms import ContactForm


def index(request):
    """
    Serves as the main entry point to the website.
    """
    return render(request, 'portfolio/index.html', {'form': ContactForm()})

class ContactView(View):
    """
    Contact view of the portfolio application.

    This view handles the rendering of the contact page and processing of the contact form.
    It displays the contact form to the user and validates the form submission. Upon 
    successful submission, it sends an email notification and redirects the user to a 
    success page.

    Attributes:
        template (str): The template to render for the contact page.
        success_url (str): The URL to redirect to after successful form submission.
        success_message (str): The success message to display upon successful form submission.
    """
    template = 'portfolio/contact.html'
    success_url = reverse_lazy('portfolio:contact')
    success_message = "Thanks for getting in touch! I'll reply to you as soon as possible."

    def get(self, request):
        """
        Serves the contact page.
        """
        form = ContactForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        """
        Validates the contact form.

        Validates the submitted contact form. If the form is valid,
        it sends an email notification, displays a success message,
        and redirects the user to the success URL. If the form is invalid,
        it renders the contact page with the form and error messages.
        """
        form = ContactForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template, context)
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        message = f"Name: {name}\nEmail: {email}\nMessage: {content}"
        send_mail(subject=subject,
                  message=message,
                  from_email=EMAIL_HOST_USER,
                  recipient_list=["enansaifme33@gmail.com"],
                  fail_silently=True)
        _ = list(messages.get_messages(request))
        messages.success(request, self.success_message)
        return redirect(self.success_url)
