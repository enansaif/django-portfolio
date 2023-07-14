"""
LeetQuizzer application views.
"""
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Count
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from leetquizzer.models import Problem, Topic, Difficulty
from leetquizzer.forms import CreateProblemForm, CreateTopicForm, UpdateProblemForm
from leetquizzer.utils.functions import get_question_list, generate_webpage
from leetquizzer.utils.functions import get_problem_info, get_problem_desc


class MainMenu(View):
    """
    View class for the main menu page.

    This class-based view handles the GET request for the main menu page.
    It retrieves a list of problems from the database and renders the 'leetquizzer/index.html' 
    template. The list of problems can be sorted based on the specified 'sorted_by' parameter, 
    which can be 'topic', 'difficulty', or None.
    """
    failure_url = 'leetquizzer/base.html'
    template = 'leetquizzer/index.html'
    def get(self, request, sorted_by=None):
        """
        Handle GET request for the main menu page.

        Args:
            sorted_by (str, optional): The sorting parameter. Can be 'topic', 'difficulty', or None.

        Returns:
            HttpResponse: The rendered response with the 'leetquizzer/index.html' template and the 
            problem list context.

        Note:
            The 'sorted_by' parameter determines the sorting order of the problem list.
            If 'sorted_by' is 'topic', the problems are sorted by topic name.
            If 'sorted_by' is 'difficulty', the problems are sorted by difficulty name.
            If 'sorted_by' is None, the problems are sorted by time (default order).
        """
        try:
            if sorted_by:
                problems = Problem.objects.order_by(sorted_by)
            else:
                problems = Problem.objects.order_by('time')
            context = {'problem_list': problems, 'current': sorted_by}
            return render(request, self.template, context)
        except FieldError:
            return render(request, self.failure_url)


class ProblemMenu(View):
    """
    This class-based view handles the GET and POST requests for the problem menu page.
    It retrieves a specific problem from the database and renders the corresponding 
    flashcard template.
    """
    success_url = reverse_lazy('leetquizzer:main_menu')
    template = "leetquizzer/problem.html"
    def get(self, request, problem_id):
        """
        Handle GET request for the problem menu page.

        Args:
            problem_id (int): The ID of the problem to display.

        Returns:
            HttpResponse: The rendered response with the corresponding quiz template and the 
            question list context.
        """
        problem = get_object_or_404(Problem, pk=problem_id)
        question_list = get_question_list(problem)
        context = {'question_list': question_list, 'problem_link': problem.link,
                   'quiz_url': f'quizzes/{problem.number}-{problem.name}.html'}
        return render(request, self.template, context)

    def post(self, request, problem_id):
        """
        Handle POST request for the problem menu page.

        Args:
            problem_id (int): The ID of the problem.

        Returns:
            HttpResponseRedirect: Redirects to the current page after processing the POST request.
        """
        problem = get_object_or_404(Problem, pk=problem_id)
        form_dict = request.POST.dict()
        form_dict.pop('csrfmiddlewaretoken')
        is_wrong = False
        for value in form_dict.values():
            if value == '0':
                is_wrong = True
        problem.wrong = is_wrong
        problem.save()
        return redirect(self.success_url)


class CreateProblem(LoginRequiredMixin, View):
    """
    View class for creating a new problem.

    This class-based view handles the GET and POST requests for creating a new problem.
    It renders the 'problem_create.html' template for displaying the form to create a problem.
    The view performs form validation, checks for existing problems with the same name or number,
    and saves the new problem to the database if it passes all validations.

    Attributes:
        template (str): The name of the template to render.
        success_url (str): The URL to redirect to after successfully creating the problem.
        failure_url (str): The URL to redirect to after failed creating the problem.
    """
    template = 'leetquizzer/problem_create.html'
    failure_url = 'leetquizzer/base.html'
    success_url = reverse_lazy('leetquizzer:main_menu')
    root_path = 'leetquizzer/templates/quizzes/'
    def get(self, request):
        """
        Handle GET request for creating a new problem.
        """
        form = CreateProblemForm()
        context = {'form': form, 'page_title': 'Create Problem'}
        return render(request, self.template, context)
    def post(self, request):
        """
        Handle POST request for creating a new problem.

        Returns:
            HttpResponseRedirect: Redirects to the success URL after creating the problem.
            HttpResponse: The rendered response with the create problem form and error message 
            if form validation fails.

        Note:
            This method performs form validation by checking if the form is valid.
            If the form is not valid, it re-renders the template with the form and appropriate 
            error messages. It then checks if a problem with the same name or number already 
            exists in the database. If a problem with the same name or number exists, it re-renders 
            the template with the form and an error message. If the form passes all validations, 
            a new Problem instance is created and saved to the database. The response is redirected 
            to the success URL.
        """
        form = CreateProblemForm(request.POST)
        if not form.is_valid():
            context = {'form': form, 'page_title': 'Create Problem'}
            return render(request, self.template, context)
        question_link = form.cleaned_data['link']
        endpoints = question_link.split('/')
        info_dict = get_problem_info(endpoints[-2])
        if not info_dict:
            return redirect(self.failure_url)
        number = info_dict['questionFrontendId']
        has_number = Problem.objects.filter(number=number).exists()
        if has_number:
            context = {'form': form, 'page_title': 'Create Problem',
                       'message': 'Problem already exists!'}
            return render(request, self.template, context)
        difficulty, _ = Difficulty.objects.get_or_create(name=info_dict['difficulty'])
        problem = Problem(link=endpoints[-2],
                          difficulty=difficulty,
                          number=number,
                          name=info_dict['title'],
                          topic=form.cleaned_data['topic'],
                          edge_case=form.cleaned_data['edge_case'],
                          solution=form.cleaned_data['solution'],
                          option1=form.cleaned_data['option1'],
                          option2=form.cleaned_data['option2'])
        problem.save()
        content = get_problem_desc(endpoints[-2]).get('content', {})
        generate_webpage(content, problem, self.root_path)
        return redirect(self.success_url)


class UpdateProblem(LoginRequiredMixin, View):
    """
    A class-based view for updating a problem object.

    Attributes:
        template (str): The path to the template used for rendering the update form.
        success_url (str): The URL to redirect to after successfully updating the problem.
    """
    template = 'leetquizzer/problem_create.html'
    success_url = reverse_lazy('leetquizzer:main_menu')
    def get(self, request, problem_id):
        """
        Retrieves the problem object with the given problem_id and renders the update form
        with pre-filled data based on the problem's current values.

        Args:
            problem_id (int): The ID of the problem to be updated.
        """
        problem = get_object_or_404(Problem, pk=problem_id)
        initial_dict = {
        "topic": problem.topic,
        "solution": problem.solution,
        "edge_case": problem.edge_case,
        "option1": problem.option1,
        "option2": problem.option2,
        }
        form = UpdateProblemForm(initial=initial_dict)
        context = {'form': form, 'page_title': 'Update Problem'}
        return render(request, self.template, context)
    def post(self, request, problem_id):
        """
        Handles the form submission and updates the problem object with the submitted data.

        Args:
            request (HttpRequest): The HTTP request object.
            problem_id (int): The ID of the problem to be updated.
        """
        form = UpdateProblemForm(request.POST)
        if not form.is_valid():
            context = {'form': form, 'page_title': 'Update Problem'}
            return render(request, self.template, context)
        problem = get_object_or_404(Problem, pk=problem_id)
        problem.topic = form.cleaned_data['topic']
        problem.edge_case = form.cleaned_data['edge_case']
        problem.solution = form.cleaned_data['solution']
        problem.option1 = form.cleaned_data['option1']
        problem.option2 = form.cleaned_data['option2']
        problem.save()
        return redirect(self.success_url)


class DeleteProblem(LoginRequiredMixin, View):
    """
    Class to handle deleting a problem
    """
    success_url = reverse_lazy('leetquizzer:main_menu')
    root_path = 'leetquizzer/templates/quizzes/'
    def post(self, _, problem_id):
        """
        Get the problem form database and delete it
        """
        problem = get_object_or_404(Problem, pk=problem_id)
        problem.delete()
        file_path = self.root_path + f'{problem.number}-{problem.name}.html'
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(self.success_url)


class CreateTopic(View):
    """
    View class for creating a new topic.

    This class-based view handles the GET and POST requests for creating a new topic.
    It renders the 'topic_create.html' template for displaying the form to create a topic.
    The view performs form validation, checks for existing topics with the same name,
    and saves the new topic to the database if it passes all validations.

    Attributes:
        template (str): The name of the template to render.
        success_url (str): The URL to redirect to after successfully creating the topic.
    """
    template = 'leetquizzer/topic_create.html'
    success_url = reverse_lazy('leetquizzer:create_problem')
    def get(self, request):
        """
        Handle GET request for creating a new topic.
        """
        form = CreateTopicForm()
        topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
        context = {'page_title': 'Create Topic', 'form': form, 'topic_list': topics}
        return render(request, self.template, context)
    def post(self, request):
        """
        Handle POST request for creating a new topic.

        Returns:
            HttpResponseRedirect: Redirects to the success URL after creating the topic.
            HttpResponse: The rendered response with the create topic form and error message 
            if form validation fails.

        Note:
            This method performs form validation by checking if the form is valid. If the form 
            is not valid, it re-renders the template with the form and appropriate error messages.
            It then checks if a topic with the same name already exists in the database. If a 
            topic with the same name exists, it re-renders the template with the form and an 
            error message. If the form passes all validations, a new Topic instance is created 
            and saved to the database. The response is redirected to the success URL.
        """
        form = CreateTopicForm(request.POST)
        if not form.is_valid():
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'page_title': 'Create Topic', 'form': form, 'topic_list': topics}
            return render(request, self.template, context)
        new_topic = form.cleaned_data['topic'].lower().title()
        has_topic = Topic.objects.filter(name=new_topic).exists()
        if has_topic:
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'page_title': 'Create Topic', 'form': form, 'topic_list': topics,
                       'message': 'Topic with this name already exists!'}
            return render(request, self.template, context)
        topic = Topic(name=new_topic)
        topic.save()
        return redirect(self.success_url)


class UpdateTopic(View):
    """
    View class for creating a new topic.
    """
    template = 'leetquizzer/topic_create.html'
    success_url = reverse_lazy('leetquizzer:main_menu')
    def get(self, request, topic_id):
        """
        Handle GET request for creating a new topic.
        """
        topic = get_object_or_404(Topic, pk=topic_id)
        init_dict = {'topic': topic}
        form = CreateTopicForm(initial=init_dict)
        topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
        context = {'page_title': 'Update Topic', 'form': form, 'topic_list': topics}
        return render(request, self.template, context)
    def post(self, request, topic_id):
        """
        Handle POST request for creating a new topic.
        """
        form = CreateTopicForm(request.POST)
        if not form.is_valid():
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'page_title': 'Update Topic', 'form': form, 'topic_list': topics}
            return render(request, self.template, context)
        new_topic = form.cleaned_data['topic'].lower().title()
        has_topic = Topic.objects.filter(name=new_topic).exists()
        if has_topic:
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'page_title': 'Update Topic', 'form': form, 'topic_list': topics,
                       'message': 'Topic with this name already exists!'}
            return render(request, self.template, context)
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.name = new_topic
        topic.save()
        return redirect(self.success_url)
