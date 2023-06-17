from django.shortcuts import render, redirect
from django.db.models import Count
from django.views import View
from django.urls import reverse_lazy
from leetquizzer.models import Problem, Topic, Difficulty
from leetquizzer.forms import AddProblemForm, AddTopicForm, AddDifficultyForm


class MainMenu(View):
    def get(self, request):
        problems = Problem.objects.all()
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)

class AddProblem(View):
    template = 'leetquizzer/create.html'
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
        problem = Problem(name=form.cleaned_data['name'], 
                          number=form.cleaned_data['number'],
                          topic=form.cleaned_data['topic'], 
                          difficulty=form.cleaned_data['difficulty'],
                          solution=form.cleaned_data['solution'], 
                          edge_case=form.cleaned_data['edge_case'])
        problem.save()
        return redirect(self.success_url)

class AddTopic(View):
    template = 'leetquizzer/add_topic.html'
    success_url = reverse_lazy('leetquizzer:create')
    
    def get(self, request):
        form = AddTopicForm()
        topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
        print(topics)
        context = {'form': form, 'topic_list': topics}
        return render(request, self.template, context)
    
    def post(self, request):
        form = AddTopicForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template, context)
        topic = Topic(name=form.cleaned_data['topic'])
        topic.save()
        return redirect(self.success_url)

class AddDifficulty(View):
    template = 'leetquizzer/add_difficulty.html'
    success_url = reverse_lazy('leetquizzer:create')
    
    def get(self, request):
        form = AddDifficultyForm()
        context = {'form': form}
        return render(request, self.template, context)
    
    def post(self, request):
        form = AddDifficultyForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, self.template, context)
        difficulty = Difficulty(name=form.cleaned_data['difficulty'])
        difficulty.save()
        return redirect(self.success_url)
        
