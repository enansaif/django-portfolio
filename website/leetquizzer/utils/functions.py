import random
import openai
from collections import deque
from website.settings import OPENAI_ORGANIZATION, OPENAI_API_KEY
from leetquizzer.models import Problem, Difficulty

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
    that is guaranteed to be included in the list. The function then randomly selects additional
    problems until the desired number of questions is reached. Each question's solution is added
    to the list as a tuple, along with a string indicating whether the solution is right or wrong.
    If available, the optional choices (option1 and option2) of the problems are also included.
    The final list is shuffled to randomize the order of the questions.
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
    """
    if Difficulty.objects.count() < len(levels):
        for level in levels:
            difficulty, _ = Difficulty.objects.get_or_create(name=level)
            difficulty.save()

def generate_HTML(problem):
    openai.organization = OPENAI_ORGANIZATION
    openai.api_key = OPENAI_API_KEY
    content = problem.link + "generate an HTML page using the problem description from the link."
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": content}],
    temperature = 1)

    html = completion.choices[0].message.content
    lines = deque(html.splitlines())
    while lines[0] != '<body>':
        lines.popleft()
    while lines[-1] != '</body>':
        lines.pop()
    file_path = 'leetquizzer/templates/quizzes/' + f'{problem.number}.html'
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line)