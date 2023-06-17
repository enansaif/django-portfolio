from django.shortcuts import render

def base(request):
    return render(request, 'portfolio/base.html')

def about(request):
    return render(request, 'portfolio/about.html')

def resume(request):
    return render(request, 'portfolio/resume.html')

def projects(request):
    return render(request, 'portfolio/projects.html')

def contact(request):
    return render(request, 'portfolio/contact.html')
