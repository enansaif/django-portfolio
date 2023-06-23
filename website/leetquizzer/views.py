"""
LeetQuizzer application views.
"""
import random
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Count
from django.views import View
from django.template.exceptions import TemplateDoesNotExist
from django.contrib import messages
from django.db.utils import OperationalError
from leetquizzer.models import Problem, Topic, Difficulty
from leetquizzer.forms import CreateProblemForm, CreateTopicForm

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

def set_difficulty(levels):
    """
    Set difficulty levels in the database.

    Args:
        levels (list): A list of difficulty level names.

    This function sets the difficulty levels in the database by creating or retrieving the 
    Difficulty objects. It takes a list of difficulty level names as input.

    If the number of existing Difficulty objects in the database is less than the length of 
    the provided 'levels' list, it iterates over each level in the 'levels' list and creates 
    a new Difficulty object if it doesn't already exist. The 'name' attribute of the Difficulty 
    object is set using the level name from the list.

    After creating or retrieving the Difficulty objects, they are saved to the database.

    Note:
        Make sure to properly configure the models and database connection before running this 
        function.

    Example:
        set_difficulty(['Easy', 'Medium', 'Hard'])  # Sets the difficulty levels in the database.
    """
    if Difficulty.objects.count() < len(levels):
        for level in levels:
            difficulty, _ = Difficulty.objects.get_or_create(name=level)
            difficulty.save()


class MainMenu(View):
    """
    View class for the main menu page.

    This class-based view handles the GET request for the main menu page.
    It retrieves a list of problems from the database and renders the 'leetquizzer/index.html' 
    template. The list of problems can be sorted based on the specified 'sorted_by' parameter, 
    which can be 'topic', 'difficulty', or None.
    """
    def get(self, request, sorted_by=None):
        """
        Handle GET request for the main menu page.

        Args:
            request (HttpRequest): The HTTP request object.
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
        if sorted_by == 'topic':
            problems = Problem.objects.order_by('topic__name')
        elif sorted_by == 'difficulty':
            problems = Problem.objects.order_by('difficulty__name')
        else:
            problems = Problem.objects.order_by('time')
        context = {'problem_list': problems}
        return render(request, 'leetquizzer/index.html', context)


class ProblemMenu(View):
    """
    View class for the problem menu page.

    This class-based view handles the GET and POST requests for the problem menu page.
    It retrieves a specific problem from the database and renders the corresponding quiz template.
    The view supports storing and retrieving question lists in the session for each problem.

    Attributes:
        failure_url (str): The URL of the base template to render in case of failure.
        success_message (str): The success message to display when the answer is correct.
        failure_message (str): The failure message to display when the answer is incorrect.
    """
    failure_url = 'quizzes/base.html'
    success_message = "ABSOLUTELY CORRECT!!!"
    failure_message = "WRONG!!! please try again later"
    def get(self, request, problem_id):
        """
        Handle GET request for the problem menu page.

        Args:
            request (HttpRequest): The HTTP request object.
            problem_id (int): The ID of the problem to display.

        Returns:
            HttpResponse: The rendered response with the corresponding quiz template and the 
            question list context.

        Note:
            This method retrieves the problem from the database based on the provided 'problem_id'.
            If the question list for the problem is not stored in the session, it generates a new 
            question list using the 'make_list' function.The rendered template depends on the 
            problem's 'number' attribute. The question list is stored in the session using the 
            'problem_id' as the key.
        """
        try:
            problem = Problem.objects.get(pk=problem_id)
            key = f"q{problem_id}"
            if key not in request.session:
                q_list = make_list(num_questions=4, problem=problem)
                request.session[key] = q_list
            context = {'question_list': request.session[key]}
            return render(request, f"quizzes/{problem.number}.html", context)
        except TemplateDoesNotExist:
            return render(request, self.failure_url)
    def post(self, request, problem_id):
        """
        Handle POST request for the problem menu page.

        Args:
            request (HttpRequest): The HTTP request object.
            problem_id (int): The ID of the problem.

        Returns:
            HttpResponseRedirect: Redirects to the current page after processing the POST request.

        Note:
            This method retrieves the problem from the database based on the provided 'problem_id'.
            The answer is retrieved from the request's POST data. The question list for the problem 
            is removed from the session. The success or failure messages are stored in the messages 
            framework based on the correctness of the answer. The 'wrong' attribute of the problem 
            object is updated accordingly and saved. The response is redirected back to the current 
            page.
        """
        problem = Problem.objects.get(pk=problem_id)
        key = f"q{problem_id}"
        answer = request.POST.get('answer', None)
        request.session.pop(key)
        _ = list(messages.get_messages(request))
        if answer == 'True':
            messages.info(request, self.success_message)
            problem.wrong = False
        else:
            messages.info(request, self.failure_message)
            problem.wrong = True
        problem.save()
        return redirect(self.request.path_info)


class CreateProblem(View):
    """
    View class for creating a new problem.

    This class-based view handles the GET and POST requests for creating a new problem.
    It renders the 'create_problem.html' template for displaying the form to create a problem.
    The view performs form validation, checks for existing problems with the same name or number,
    and saves the new problem to the database if it passes all validations.

    Attributes:
        template (str): The name of the template to render.
        success_url (str): The URL to redirect to after successfully creating the problem.
    """
    try:
        set_difficulty(('Easy', 'Medium', 'Hard'))
    except OperationalError:
        pass
    template = 'leetquizzer/create_problem.html'
    success_url = reverse_lazy('leetquizzer:main_menu')
    def get(self, request):
        """
        Handle GET request for creating a new problem.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered response with the create problem form.

        Note:
            This method creates a new instance of the CreateProblemForm and passes it as context 
            to the template. The template is rendered with the form to allow the user to input 
            the problem details.
        """
        form = CreateProblemForm()
        context = {'form': form}
        return render(request, self.template, context)
    def post(self, request):
        """
        Handle POST request for creating a new problem.

        Args:
            request (HttpRequest): The HTTP request object.

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
            context = {'form': form}
            return render(request, self.template, context)
        has_name = Problem.objects.filter(name=form.cleaned_data['name']).exists()
        has_number = Problem.objects.filter(number=form.cleaned_data['number']).exists()
        if has_name or has_number:
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


class CreateTopic(View):
    """
    View class for creating a new topic.

    This class-based view handles the GET and POST requests for creating a new topic.
    It renders the 'create_topic.html' template for displaying the form to create a topic.
    The view performs form validation, checks for existing topics with the same name,
    and saves the new topic to the database if it passes all validations.

    Attributes:
        template (str): The name of the template to render.
        success_url (str): The URL to redirect to after successfully creating the topic.

    Methods:
        get(request): Handles the GET request for creating a new topic.
        post(request): Handles the POST request for creating a new topic.
    """
    template = 'leetquizzer/create_topic.html'
    success_url = reverse_lazy('leetquizzer:create_problem')
    def get(self, request):
        """
        Handle GET request for creating a new topic.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered response with the create topic form and the list of existing 
            topics.

        Note:
            This method creates a new instance of the CreateTopicForm and retrieves the list of 
            existing topics. The template is rendered with the form and the list of topics to 
            allow the user to input the topic details.
        """
        form = CreateTopicForm()
        topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
        context = {'form': form, 'topic_list': topics}
        return render(request, self.template, context)
    def post(self, request):
        """
        Handle POST request for creating a new topic.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the success URL after creating the topic.
            HttpResponse: The rendered response with the create topic form and error message 
            if form validation fails.

        Raises:
            None

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
            context = {'form': form, 'topic_list': topics}
            return render(request, self.template, context)
        new_topic = form.cleaned_data['topic'].lower().title()
        has_topic = Topic.objects.filter(name=new_topic).exists()
        if has_topic:
            topics = Topic.objects.annotate(Count('problem')).values_list('name', 'problem__count')
            context = {'form': form, 'topic_list': topics,
                       'message': 'Topic with this name already exists!'}
            return render(request, self.template, context)
        topic = Topic(name=new_topic)
        topic.save()
        return redirect(self.success_url)
