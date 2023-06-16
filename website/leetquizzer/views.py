from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from leetquizzer.models import Problem
from leetquizzer.forms import AddProblemForm


class MainMenu(View):
    def get(self, request):
        problems = Problem.objects.all()
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)

class AddProblem(View):
    template = 'leetquizzer/add.html'
    success_url = reverse_lazy('leetquizzer:main_menu')
    
    def get(self, request):
        form = AddProblemForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = AddProblemForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template, context)
        problem = form.save()
        return redirect(self.success_url)
        
