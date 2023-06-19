import csv
from leetquizzer.models import Problem, Topic, Difficulty

def run():
    file = open("leetquizzer/data/problems.csv")
    reader = csv.reader(file)
    next(reader)
    
    count = 0
    for row in reader:
        number, name = row[0], row[1]
        hasNumber = Problem.objects.filter(number=number).exists()
        hasName = Problem.objects.filter(name=name).exists()
        if hasNumber or hasName:
            continue
        topic, _ = Topic.objects.get_or_create(name=row[2])
        difficulty, _ = Difficulty.objects.get_or_create(name=row[3])
        
        problem = Problem(number=number, name=name, topic=topic, difficulty=difficulty, 
                          solution=row[4], option1=row[5], option2=row[6], edge_case=row[7])
        problem.save()
        count += 1
    
    print(f"{count} Problems added to Database")