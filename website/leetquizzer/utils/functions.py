"""
All utility functions used by leetquizzer application's views.py
"""
from ast import literal_eval
import random
import openai
import requests
from openai.error import RateLimitError
from requests.exceptions import ReadTimeout
from leetquizzer.models import Difficulty
from website.settings import OPENAI_ORGANIZATION, OPENAI_API_KEY, LEETCODE_URL

def make_list(problem):
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
    question_list.append((problem.solution, right))
    if problem.option1:
        question_list.append((problem.option1, wrong))
    if problem.option2:
        question_list.append((problem.option2, wrong))
    random.shuffle(question_list)
    return question_list

def make_qa_list(problem):
    """
    Creates a question answer list for a given problem.
    """
    questions = []
    if problem.option1:
        questions.append({'question': 'What will be the brute force approach?',
                          'answer': problem.option1})
    if problem.option2:
        questions.append({'question': 'Can you improve uppon the brute force approach?',
                          'answer': problem.option2})
    questions.append({'question': 'What is the most efficient approach?',
                      'answer': problem.solution})
    return questions

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
        with open(file_path, 'w', encoding="utf-8") as html_file:
            for prefix in prefixes:
                html_file.writelines([prefix, '\n'])
            for line in lines[start + 1:end]:
                html_file.writelines([line, '\n'])
            for suffix in suffixes:
                html_file.writelines([suffix, '\n'])

def send_query(query):
    """
    Sends a query to graphql server of leetcode. If response is valid, returns response else
    returns an empty dictionary.
    """
    try:
        response = requests.post(url=LEETCODE_URL, json=query, timeout=5)
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

def get_info(title_slug):
    """
    Retrieve information about a question from LeetCode API based on its title slug.

    Args:
        title_slug (str): The title slug of the question.

    Returns:
        dict: A dictionary containing the question information including questionFrontendId, 
        title, and difficulty. If the request fails or the response is invalid, an empty 
        dictionary is returned.
    """
    info_query = {
        "query":"""
            query questionTitle($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionFrontendId
                    title
                    difficulty
                }
            }
        """,
        "variables": {"titleSlug":f'{title_slug}'},
        "operationName": "questionTitle"
    }
    return send_query(info_query)

def get_problem_description(title_slug):
    """
    Retrieve problem description from LeetCode API based on its title slug.
    """
    description_query = {
        "query":"""
            query questionTitle($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    content
                }
            }
        """,
        "variables": {"titleSlug":f'{title_slug}'}, 
        "operationName": "questionTitle"
    }
    return send_query(description_query)

def generate_webpage(content, problem, root_path):
    """
    Generate a webpage for a given problem with the provided content.

    Parameters:
    - content (str): The content of the webpage.
    - problem: An object representing the problem, containing attributes like `number` and `name`.

    This function generates a webpage for a given problem by writing the content
    into an HTML file. The file is created based on the problem's number and stored
    in the 'leetquizzer/templates/quizzes' directory.

    Note: The function assumes the existence of base HTML templates to properly
    structure the generated webpage.
    """
    title = f"<h1>{problem.number} - {problem.name}</h1>"
    file_path = root_path + f'{problem.number}.html'
    with open(file_path, 'w', encoding="utf-8") as html_file:
        html_file.writelines([title, '\n'])
        for line in content.splitlines():
            html_file.writelines([line, '\n'])
            