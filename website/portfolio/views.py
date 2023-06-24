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

def base(request):
    """
    Serves as the main entry point to the website.
    """
    return render(request, 'portfolio/base.html')

def about(request):
    """
    Serves the about page.
    """
    return render(request, 'portfolio/code.html')

def resume(request):
    """
    Serves the resume page.
    """
    return render(request, 'portfolio/resume.html')

def project_info():
    """
    Retrieve information about projects.

    Returns:
        list: A list of dictionaries containing project information.

    This function retrieves information about projects and returns it as a list of dictionaries.
    Each dictionary represents a project and contains the following keys:
    - 'name': The name of the project.
    - 'description': A description of the project.
    - 'tools': A list of tools/technologies used in the project.
    - 'url': The URL or route for accessing the project.

    Note:
        Make sure to import the 'reverse' in order to generate the 'url' value.
    """
    project_list = []
    leetquizzer = {
        'name': 'Leetquizzer',
        'description': 'A CRUD application for a quick review of my previously solved questions.',
        'tools': ['Python', 'Django', 'Bootstrap'],
        'url': reverse('leetquizzer:main_menu'),
    }
    project_list.append(leetquizzer)
    return project_list

def projects(request):
    """
    Serves the projects page with a list of projects.
    """
    context = {'project_list': project_info()}
    return render(request, 'portfolio/projects.html', context)


class ContactView(View):
    """
    Contact view of the portfolio application.
    """
    template = 'portfolio/contact.html'
    success_url = reverse_lazy('portfolio:contact')
    success_message = "Thanks for getting in touch I'll reply to you as soon as possible"
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
