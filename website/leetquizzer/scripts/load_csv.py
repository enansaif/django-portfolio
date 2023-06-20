import csv, argparse
from leetquizzer.models import Problem, Topic, Difficulty

def run(filename):
    file = open(f"leetquizzer/data/{filename}")
    reader = csv.reader(file)
    next(reader)
    
    count = 0
    for row in reader:
        number, name = row[0], row[1]
        hasNumber = Problem.objects.filter(number=number).exists()
        hasName = Problem.objects.filter(name=name).exists()
        if hasNumber or hasName:
            continue
        topic, _ = Topic.objects.get_or_create(name=row[3])
        difficulty, _ = Difficulty.objects.get_or_create(name=row[4])
        
        problem = Problem(number=number, name=name, link=row[2], topic=topic, difficulty=difficulty, 
                          solution=row[5], option1=row[6], option2=row[7], edge_case=row[8])
        problem.save()
        count += 1
    
    print(f"{count} Problems added to Database")