from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Count
from django.views import View
from django.template.exceptions import TemplateDoesNotExist
from leetquizzer.models import Problem, Topic, Difficulty
from leetquizzer.forms import AddProblemForm, AddTopicForm, AddDifficultyForm


class MainMenu(View):
    def get(self, request):
        problems = Problem.objects.all()
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)


class TopicMenu(View):
    def get(self, request):
        problems = Problem.objects.order_by('topic__name')
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)


class DifficultyMenu(View):
    def get(self, request):
        problems = Problem.objects.order_by('difficulty__name')
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)


class ProblemMenu(View):
    def get(self, request, problem_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            context = {'problem': problem}
            return render(request, f"quizzes/{problem.number}.html", context)
        except TemplateDoesNotExist:
            return render(request, 'quizzes/base.html')


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
        
        hasName = Problem.objects.filter(name=form.cleaned_data['name']).exists()
        hasNumber = Problem.objects.filter(number=form.cleaned_data['number']).exists()
        if hasName or hasNumber:
            context = {'form': form,
                       'message': 'Problem with this name or number already exists!'}
            return render(request, self.template, context)
        
        problem = Problem(name=form.cleaned_data['name'], 
                          number=form.cleaned_data['number'],
                          topic=form.cleaned_data['topic'], 
                          difficulty=form.cleaned_data['difficulty'],
                          edge_case=form.cleaned_data['edge_case'],
                          solution=form.cleaned_data['solution'],
                          option1=form.cleaned_data['option1'],
                          option2=form.cleaned_data['option2'])
        problem.save()
        return redirect(self.success_url)


class AddTopic(View):
    template = 'leetquizzer/add_topic.html'
    success_url = reverse_lazy('leetquizzer:create')
    
    def get(self, request):
        form = AddTopicForm()
        topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
        context = {'form': form, 'topic_list': topics}
        return render(request, self.template, context)
    
    def post(self, request):
        form = AddTopicForm(request.POST)
        if not form.is_valid():
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'form': form, 'topic_list': topics}
            return render(request, self.template, context)
        
        new_topic = form.cleaned_data['topic']
        hasTopic = Topic.objects.filter(name=new_topic).exists()
        if hasTopic:
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'form': form, 'topic_list': topics, 
                       'message': 'Topic with this name already exists!'}
            return render(request, self.template, context)
        
        topic = Topic(name=new_topic)
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
        
