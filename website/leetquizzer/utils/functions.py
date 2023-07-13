"""
All utility functions used by leetquizzer application's views.py
"""
import ast
import requests
from requests.exceptions import ReadTimeout
from website.settings import LEETCODE_URL

def get_question_list(problem):
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

def send_query(query):
    """
    Sends a query to graphql server of leetcode. If response is valid, returns response else
    returns an empty dictionary.
    """
    try:
        response = requests.post(url=LEETCODE_URL, json=query, timeout=5)
        if response.status_code == 200:
            try:
                response_dict = ast.literal_eval(response.content.decode('utf-8'))
                return response_dict['data']['question']
            except ValueError:
                print("Error while decoding")
        else:
            print("Didn't get response")
    except ReadTimeout:
        print("Request Timeout")
    return {}

def get_problem_info(title_slug):
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

def get_problem_desc(title_slug):
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
    file_path = root_path + f'{problem.number}-{problem.name}.html'
    with open(file_path, 'w', encoding="utf-8") as html_file:
        html_file.writelines([title, '\n'])
        for line in content.splitlines():
            html_file.writelines([line, '\n'])
            