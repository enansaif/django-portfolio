"""
Delivers the views related to authentication
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """
    View for handling logout requests
    """
    success_url = reverse_lazy('portfolio:base')
    logout(request)
    return redirect(request.GET.get('next', success_url))


class LoginUser(View):
    """
    View class for handling user login.

    GET: Renders the login form.

    POST: Authenticates the user with the provided username and password.
    If the authentication is successful, logs in the user and redirects to the request URL.
    Otherwise, displays an error message and redirects back to the login page.
    """
    success_url = reverse_lazy('portfolio:base')

    def get(self, request):
        """
        Handles GET requests to render the login form.
        """
        return render(request, 'auth/login.html')

    def post(self, request):
        """
         Handles POST requests to authenticate the user.
        """
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', self.success_url))
        messages.error(request, "Invalid username or password")
        return redirect(self.request.path_info)


class Signup(View):
    success_url = reverse_lazy('portfolio:base')

    def get(self, request):
        form = UserCreationForm()
        return render(request, "auth/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', self.success_url))
        return redirect(self.request.path_info)
