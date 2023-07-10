"""
All utility functions used by leetquizzer application's views.py
"""
import random
import openai
import requests
from ast import literal_eval
from openai.error import RateLimitError
from requests.exceptions import ReadTimeout
from leetquizzer.models import Problem, Difficulty
from website.settings import OPENAI_ORGANIZATION, OPENAI_API_KEY, LEETCODE_URL

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

def generate_webpage_gpt(problem):
    """
    Generates an HTML page using the problem description from the provided link.

    The function utilizes the OpenAI GPT-3.5 Turbo model to generate the HTML content
    based on the problem description obtained from the link. It then writes the generated
    content to an HTML file with a filename corresponding to the problem number.

    Args:
        problem (Problem): The problem object containing the link to the problem description.

    Raises:
        RateLimitError: If the rate limit for the OpenAI API is exceeded.
    """
    openai.organization = OPENAI_ORGANIZATION
    openai.api_key = OPENAI_API_KEY
    content = problem.link + " generate an HTML page using the problem description from the link."
    try:
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        temperature = 1)
    except RateLimitError:
        print('Rate limit for the OpenAI API has exceeded!!!')
    else:
        lines = completion.choices[0].message.content.splitlines()
        start, end = lines.index('<body>'), lines.index('</body>')
        prefixes = ['{% extends "quizzes/base.html" %}', '{% block quiz %}', '<div>']
        suffixes = ['</div>', '{% include "quizzes/q_snippet.html" %}', '{% endblock %}']
        file_path = 'leetquizzer/templates/quizzes/' + f'{problem.number}.html'
        with open(file_path, 'w', encoding="utf-8") as f:
            for prefix in prefixes:
                f.write(prefix)
                f.write('\n')
            for line in lines[start + 1:end]:
                f.write(line)
                f.write('\n')
            for suffix in suffixes:
                f.write(suffix)
                f.write('\n')

def get_info(title_slug):
    """
    Retrieve information about a question from LeetCode API based on its title slug.

    Args:
        title_slug (str): The title slug of the question.

    Returns:
        dict: A dictionary containing the question information including questionFrontendId, 
        title, titleSlug, difficulty, and content. If the request fails or the response is 
        invalid, an empty dictionary is returned.
    """
    info_query = {
        "query":"""
            query questionTitle($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                    content
                }
            }
        """,
        "variables": {"titleSlug":f'{title_slug}'}, 
        "operationName": "questionTitle"
    }
    try:
        response = requests.post(url=LEETCODE_URL, json=info_query, timeout=5)
        if response.status_code == 200:
            try:
                response_dict = literal_eval(response.content.decode('utf-8'))
                return response_dict['data']['question']
            except ValueError:
                print("Error while decoding")
        else:
            print("Didn't get response")
    except ReadTimeout:
        print("Request Timeout")
    return {}

def generate_webpage(content, problem):
    lines = content.splitlines()
    prefixes = ['{% extends "quizzes/base.html" %}', '{% block quiz %}', '<div>']
    suffixes = ['</div>', '{% include "quizzes/q_snippet.html" %}', '{% endblock %}']
    file_path = 'leetquizzer/templates/quizzes/' + f'{problem.number}.html'
    with open(file_path, 'w', encoding="utf-8") as f:
        for prefix in prefixes:
            f.write(prefix)
            f.write('\n')
        for line in lines:
            f.write(line)
            f.write('\n')
        for suffix in suffixes:
            f.write(suffix)
            f.write('\n')
            