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
    return render(request, 'portfolio/about.html')


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
    """
    project_list = []
    chessai = {
        'name': 'Chess-AI',
        'description': '''Play against AI. developed using Django, the chess.py library and chessboard.js library''',
        'tools': ['Python', 'JavaScript', 'PyTorch', 'Bootstrap', 'chess.py'],
        'url': reverse('chess_app:game_view'),
        'github': 'https://github.com/enansaif/chess_project',
    }
    
    leetquizzer = {
        'name': 'Leetquizzer',
        'description': 'A CRUD application for a quick review of my previously solved questions.',
        'tools': ['Python', 'Django', 'Bootstrap', 'GraphQL', 'JavaScript'],
        'url': reverse('leetquizzer:main_menu'),
        'github': 'https://github.com/enansaif/flashcards',
    }
    portfolio = {
        'name': 'Portfolio',
        'description': '''My portfolio itself is a django app that routs to other django applications.''',
        'tools': ['Python', 'Django', 'HTML', 'CSS', 'Bootstrap'],
        'url': reverse('portfolio:base'),
        'github': 'https://github.com/enansaif/portfolio',
    }
    project_list.append(chessai)
    project_list.append(leetquizzer)
    project_list.append(portfolio)
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
