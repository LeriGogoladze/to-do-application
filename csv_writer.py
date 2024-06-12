import csv
from datetime import datetime
from task import Task, StartDateDueDateTask

# ფაილი სადაც შეინახება დავალებების შესახებ ინფომრაცია
CSV_FILE = 'tasks.csv'

# ახალი დავალების csv ფაილში ჩაწერის ფუნქცია
def save_tasks_to_csv(tasks):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['task_id', 'create_date', 'description', 'priority', 'status', 'start_date', 'due_date', 'task_type'])

        for task in tasks:
            if isinstance(task, StartDateDueDateTask):
                writer.writerow([task.task_id, task._Task__create_date.strftime("%Y-%m-%d %H:%M:%S"), task.description, task.priority, task.status, task.start_date.strftime("%Y-%m-%d"), task.due_date.strftime("%Y-%m-%d"), 'StartDateDueDateTask'])
            else:
                writer.writerow([task.task_id, task._Task__create_date.strftime("%Y-%m-%d %H:%M:%S"), task.description, task.priority, task.status, '', '', 'Task'])

# დავალებების csv ფაილიდან ამოტვირთვის ფუნქცია
def load_tasks_from_csv():
    tasks = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['task_type'] == 'StartDateDueDateTask':
                    description = row["description"]
                    start_date = datetime.strptime(row["start_date"], "%Y-%m-%d")
                    due_date = datetime.strptime(row["due_date"], "%Y-%m-%d")
                    task = StartDateDueDateTask(description,start_date,due_date)
                    task.task_id = row["task_id"]
                    task.create_date = datetime.strptime(row["create_date"], "%Y-%m-%d %H:%M:%S")
                    task.priority = row["priority"]
                    task.status = row["status"]
                else:
                    task = Task(row['description'])
                    task.task_id = row['task_id']
                    task.create_date = datetime.strptime(row['create_date'], "%Y-%m-%d %H:%M:%S")
                    task.priority = row['priority']
                    task.status = row['status']
                tasks.append(task)
    except FileNotFoundError:
        pass

    return tasks
