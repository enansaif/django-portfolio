"""
Script to add problems to the database from a google sheets file.
"""
import pandas as pd
from leetquizzer.models import Problem, Topic, Difficulty

def run():
    """
    Fetches data from a Google Spreadsheet and adds new problems to the database.

    This function reads data from a Google Spreadsheet using its sheet ID and page name.
    It retrieves the problem information from the spreadsheet and creates new Problem objects
    in the database if they don't already exist. The function uses the Problem, Topic, 
    and Difficulty models from the leetquizzer app.
    
    Note:
        Make sure the database exists.

    Command:
        python manage.py runscript load_sheet
    """
    sheet_id = '1LRFpWPj12lFnzwl--5jqnzGMbASOy8J17o9jEv4eBac'
    page_name = 'problems'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={page_name}'
    dataframe = pd.read_csv(url)
    count = 0
    for i in dataframe.index:
        number, name = dataframe['number'][i], dataframe['name'][i]
        has_number = Problem.objects.filter(number=number).exists()
        has_name = Problem.objects.filter(name=name).exists()
        if has_number or has_name:
            continue
        topic, _ = Topic.objects.get_or_create(name=dataframe['topic'][i].lower().title())
        difficulty, _ = Difficulty.objects.get_or_create(
                        name=dataframe['difficulty'][i].lower().capitalize())
        problem = Problem(number=number, name=name, link=dataframe['link'][i], topic=topic,
                          difficulty=difficulty, solution=dataframe['solution'][i],
                          option1=dataframe['option1'][i], option2=dataframe['option2'][i],
                          edge_case=dataframe['edge_case'][i])
        problem.save()
        count += 1
    print(f"{count} Problems added to Database")
    