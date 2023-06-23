from django.shortcuts import render
from django.urls import reverse

def base(request):
    return render(request, 'portfolio/base.html')

def about(request):
    return render(request, 'portfolio/about.html')

def resume(request):
    return render(request, 'portfolio/resume.html')

def project_info():
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
    context = {'project_list': project_info()}
    return render(request, 'portfolio/projects.html', context)

def contact(request):
    return render(request, 'portfolio/contact.html')
