import random
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

def make_list(num_questions, problem):
    """
    Create a list of questions with wrong/right flag for a given problem.

    Args:
        num_questions (int): The desired number of questions in the list.
        problem (Problem): The problem object representing the initial question.

    Returns:
        list: A list of tuples representing questions and their correctness.
    
    This function generates a list of questions by randomly selecting problems from a database
    and adding their solutions to the list. The provided problem object is the initial question
    that is guaranteed to be included in the result. The function then randomly selects additional
    problems until the desired number of questions is reached. Each question's solution is added
    to the list as a tuple, along with a string indicating whether the solution is right or wrong.
    If available, the optional choices (option1 and option2) of the problems are also included as
    tuples with the correctness set to wrong. The final list is shuffled to randomize the order
    of the questions.

    Note:
        This function assumes the model (Problem) with the following attributes is already imported:
        - solution: The solution to the problem/question.
        - option1: Optional choice 1 for the problem.
        - option2: Optional choice 2 for the problem.
    """
    question_list = []
    right, wrong = 'True', 'False'
    problem_count = Problem.objects.count()
    question_list.append((problem.solution, right))
    if problem.option1:
        question_list.append((problem.option1, wrong))
    if problem.option2:
        question_list.append((problem.option2, wrong))
    
    picked = set([problem.pk])
    while problem_count >= num_questions and len(question_list) < num_questions:
        index = problem.pk
        while index in picked:
            index = random.randint(1, problem_count)
        picked.add(index)
        question_list.append((Problem.objects.get(pk=index).solution, wrong))
    random.shuffle(question_list)
    return question_list

class ProblemMenu(View):
    def get(self, request, problem_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            q_list = make_list(num_questions=4, problem=problem)
            context = {'question_list': q_list}
            return render(request, f"quizzes/{problem.number}.html", context)
        except TemplateDoesNotExist:
            return render(request, 'quizzes/base.html')
    
    def post(self, request, problem_id):
        problem = Problem.objects.get(pk=problem_id)
        answer = request.POST.get('answer', None)
        success_message = "ABSOLUTELY CORRECT!!! &#128513"
        fail_message = "WRONG!!! please try again later &#129402"
        if answer == 'True':
            message = success_message
        else:
            message = fail_message
        context = {'question_list':[], 'message':message}
        return render(request, f"quizzes/{problem.number}.html", context)

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
                          link=form.cleaned_data['link'],
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
        
        new_topic = form.cleaned_data['topic'].lower().title()
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
        
        if Difficulty.objects.count() >= 3:
            context = {'form': form, 'message': 'How many more difficulty levels do you want!?! -_-'}
            return render(request, self.template, context)
            
        new_difficulty = form.cleaned_data['difficulty'].lower().capitalize()
        hasDifficulty = Difficulty.objects.filter(name=new_difficulty).exists()
        if hasDifficulty:
            context = {'form': form, 'message': 'You have already set this difficulty level'}
            return render(request, self.template, context)
        
        difficulty = Difficulty(name=new_difficulty)
        difficulty.save()
        return redirect(self.success_url)
        
