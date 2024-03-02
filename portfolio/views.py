"""
Serves all templates related to the portfolio application.
"""
import json
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from website.settings import EMAIL_HOST_USER
from django.http import JsonResponse


def index(request):
    """
    Serves as the main entry point to the website.
    """
    return render(request, 'portfolio/index.html')

def contact(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '')
        email = data.get('email', '')
        message = data.get('message', '')
        formatted_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_mail(subject='via website',
                  message=formatted_message,
                  from_email=EMAIL_HOST_USER,
                  recipient_list=["enansaifme33@gmail.com"],
                  fail_silently=True)
        return JsonResponse({'status': 'Success'})
