from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from ..db_schemas import TaskDBSchema

def analyze_task_data(db: Session):
    tasks = db.query(TaskDBSchema).all()

    titles = [task.title for task in tasks]
    descriptions = [task.description for task in tasks]
    text_data = " ".join(titles + descriptions)
    words = text_data.split()
    word_counter = Counter(words)

    completed_sequences = defaultdict(set)
    completed_titles = {task.title for task in tasks if task.status == 'completed'}

    for task in tasks:
        if task.status == 'completed':
            for other_task in completed_titles:
                if task.title != other_task:
                    completed_sequences[task.title].add(other_task)

    return word_counter, completed_sequences