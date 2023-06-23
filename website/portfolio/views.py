"""
Serves all templates related to the portfolio application.
"""
from django.shortcuts import render
from django.urls import reverse


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


def contact(request):
    """
    Serves the contact page.
    """
    return render(request, 'portfolio/contact.html')
