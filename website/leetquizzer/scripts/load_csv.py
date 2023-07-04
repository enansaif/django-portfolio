"""
Script to add problems to the database from a CSV file.
"""
import csv
from leetquizzer.models import Problem, Topic, Difficulty

def run(filename):
    """
    Add problems to the database from a CSV file.

    Args:
        filename (str): The name of the CSV file to read.

    This function reads a CSV file containing problem data and adds the problems to 
    the database. The function reads the data using the 'csv.reader' object, and 
    iterates over each row. For each row, if a problem with the same number or name 
    doesn't exist, it creates a new Problem object using the data from the row and 
    saves it to the database.

    Note: 
        The CSV file should be located in the 'leetquizzer/data/' directory.
        Make sure the database exists.

    Command:
        python manage.py runscript load_csv --script-args <str:filename>
    """
    file = open(f"leetquizzer/data/{filename}", encoding='utf-8')
    reader = csv.reader(file)
    next(reader)
    count = 0
    for row in reader:
        number, name = row[0], row[1]
        has_number = Problem.objects.filter(number=number).exists()
        has_name = Problem.objects.filter(name=name).exists()
        if has_number or has_name:
            continue
        topic, _ = Topic.objects.get_or_create(name=row[3].lower().title())
        difficulty, _ = Difficulty.objects.get_or_create(name=row[4].lower().capitalize())
        problem = Problem(number=number, name=name, link=row[2], topic=topic, difficulty=difficulty,
                          solution=row[5], option1=row[6], option2=row[7], edge_case=row[8])
        problem.save()
        count += 1
    print(f"{count} Problems added to Database")
    