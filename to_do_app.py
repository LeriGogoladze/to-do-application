from datetime import datetime
from task import Task,StartDateDueDateTask
from utils import generate_unique_id
from csv_writer import save_tasks_to_csv, load_tasks_from_csv

class ToDoApp:  
    def __init__(self): 
        self.tasks = []
        self.load_tasks()

    # ახალი დავალების შექმნა  
    def create_task(self):      
        description = input("Enter task's description: ")
        print("Chose task's priority(select number): ")  
        priority = input("\t1-Low\n\t2-Medium\n\t3-High\n\t4-Critical\n:")
        while not priority in ('1','2','3','4'):
             priority = input("Invalid priority.Enter again (1,2,3,4):")

        print("Chose task's status(select number): ")  
        status = input("\t1-Not Started\n\t2-Working on it\n\t3-Stuck\n\t4-Done\n:")
        while not status in ('1','2','3','4'):
            status = input("Invalid status. Enter again (1,2,3,4):")

        has_start_date = input("Does this task have a start date/due date? (y/n): ").lower() == 'y'
        if has_start_date:
            start_date = input("Enter start date (YYYY-MM-DD format) :")    
            try:
                start_date = datetime.strptime(start_date,"%Y-%m-%d")
            except ValueError:
                print("Invalid start date format. Please try again.")
                return
            
            due_date = input("Enter due date (YYYY-MM-DD format): ") 
            try:
                due_date = datetime.strptime(due_date,"%Y-%m-%d")
            except ValueError:
                print("Invalid due date format. Please try again.")
                return
        
        # დავალების ობიექტის ინიციალიზაცია.სულ 2 სახის დავალებაა. დავალება დაწყება-დასრულების ვადებით და დავალება ამ ვადების გარეშე
        if has_start_date:
            new_task = StartDateDueDateTask(description,start_date,due_date)
            new_task.task_id = generate_unique_id(self.tasks)
            new_task.set_priority(priority)
            new_task.set_status(status)
            self.tasks.append(new_task)
            self.save_tasks()
        else: 
            new_task = Task(description)  
            new_task.task_id = generate_unique_id(self.tasks)
            new_task.set_priority(priority)
            new_task.set_status(status)
            self.tasks.append(new_task)
            self.save_tasks()
            self.display_task(new_task,"Task created successfully!")
                                                                       
    # დავალების შესახებ ინფორმაციის გამოტანის ფუნქცია
    def display_task(self, task,prompt):
        print(prompt, end="\n")
        print(f"\tID: {task.task_id}")
        print(f"\tDescription: {task.description}")
        print(f"\tStatus: {task.status}")
        print(f"\tPriority: {task.priority}")
        if isinstance(task, StartDateDueDateTask):
            print(f"\tStart date: {task.start_date}")
            print(f"\tDue date: {task.due_date}")

     # დავალების ველების განახლება მომხარებლის არჩევანის შესაბამისად.მომხაფებლისგან შესაბამისი ინფომრაციის მიღება  
    def update_task(self):   
        if not self.tasks:
            print("There are no tasks to update yet. Please create some tasks first!")
            return
        
        task_id = input("Enter the ID of the task you want to update: ")
        found_task = self.find_task_by_id(task_id)
        if not found_task:
            print(f"Task with ID '{task_id}' not found.")
            return 

        update_description = input("Update Description (y/n): ").lower() == 'y'
        update_status = input("Update Status (y/n): ").lower() == 'y'
        update_priority = input("Update Priority (y/n): ").lower() == 'y'
        update_start_date = input("Update Start Date (y/n): ").lower() == 'y'
        update_due_date = input("Update Due Date (y/n): ").lower() == 'y'

        # აღწერის განახლება
        if update_description:
            new_description = input("Enter new description: ")
            found_task.description = new_description
        # სტატუსის განახლება
        if update_status:
            new_status = input("Choose new task's status (select number):\n\t1-Not Started\n\t2-Working on it\n\t3-Stuck\n\t4-Done\n:")
            while new_status not in ('1', '2', '3', '4'):
                new_status = input("Invalid priority. Enter again (1, 2, 3, 4): ")
            found_task.status = "Not Started" if new_status == '1' else (
                "Working on it" if new_status == '2' else (
                    "Stuck" if new_status == '3' else "Done"
                )
            )
        # პრიორიტეტის განახლება
        if update_priority:
            new_priority = input("Choose new task's priority (select number): ")
            while new_priority not in ('1', '2', '3', '4'):
                new_priority = input("Invalid priority. Enter again (1, 2, 3, 4): ")
            found_task.priority = "Low" if new_priority == '1' else (
                "Medium" if new_priority == '2' else (
                    "High" if new_priority == '3' else "Critical"
                )
            )
        # დაწყების თარიღის განახლება
        if update_start_date:
            new_start_date = input("Enter new start date (YYYY-MM-DD format): ")
            try:
                new_start_date = datetime.strptime(new_start_date, "%Y-%m-%d")
                found_task.start_date = new_start_date
            except ValueError:
                print("Invalid start date format. Please try again.")
        # -მდე თარიღის განახლება
        if update_due_date:
            new_due_date = input("Enter new due date (YYYY-MM-DD format): ")
            try:
                new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d")
                found_task.due_date = new_due_date
            except ValueError:
                print("Invalid due date format. Please try again.")
        prompt_text = "Task updated successfully!"
        # განახლებული დავალების შესახებ მომხარებლისთვის ინფომრაციის გამოტანა 
        self.display_task(found_task,prompt_text)
        # განახლებული დავალების შენახვა
        self.save_tasks()

    # დავალების მოძებნა CSV ფაილში აიდის შესაბამისად      
    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
      
    # ფაილში არსებული დავალებების დასორტირება
    def sort_task(self):
        """Sorts tasks in the To Do List based on user preference."""
        # დასასორტირებელი დავალებების შემოწმება. თუ ფაილი ცარიელი დასორტირებას აზრი არ აქვს
        if not self.tasks:
            print("There are no tasks to sort yet. Please create some tasks first!")
            return
        
        # სორტირებისთვის საჭირო კრიტერიუმების განსაზღვა
        print("\nSort Tasks By:")
        print("\t1. Description (ascending)")
        print("\t2. Priority (ascending)")
        print("\t3. Due Date (ascending)")
        print("\t4. Creation Date (ascending)")
        sort_by = input("Enter your choice (1-4): ")

        # მოხმარებლის მიერ შეყვანილი მონაცემების შემოწმება
        while sort_by not in ('1', '2', '3', '4'):
            sort_by = input("Invalid choice. Please enter a number between 1 and 4: ")

        # სორტირების ლოგიკების განსაზღვვრა, მომხარებლის არჩევანიდან გამომდინარე
        if sort_by == '1':
            sort_key = lambda task: task.description.lower() 
        elif sort_by == '2':
            sort_key = lambda task: task.priority if task.priority else "" 
        elif sort_by == '3':
            sort_key = lambda task: task.due_date if isinstance(task, StartDateDueDateTask) else datetime.max
        else:
            sort_key = lambda task: task.create_date

        # დავალბებების დასორტირება შესაბამისი ლოგიკით
        self.tasks.sort(key=sort_key)
        
        print("Tasks sorted successfully!")
    
    # მომხარებელს საშალება ეძლევა ნახოს შესასრულებელი დავალებების სია ან კონრეტული დავალება აიდის მიხედვით
    def view_task(self):
        if not self.tasks:
            print("There are no tasks to view.Please create some tasks first!")
            return
        
        user_input = input("Chose :\n\t1-All tasks\n\t2-Particular task \n:")
        while not user_input in ('1','2'):
             user_input = input("Invalid choice.Enter again (1,2):")
        
        if user_input == '1':
            for task in self.tasks:
                self.display_task(task,"Task Details :")        
        else:
            task_id = input("Enter task ID o :")
            found_task = self.find_task_by_id(task_id)
            if not found_task:
                print(f"Task with ID '{task_id}' not found.")
                return
            self.display_task(found_task,"Task Details :")

    # ფაილში არსებული დავალების წაშლა
    def delete_task(self):
        """Deletes a task from the To Do List."""
        if not self.tasks:
            print("There are no tasks to delete yet. Please create some tasks first!")
            return

        # დავალების ID-ის მიღება მომხარებლის მხრიდან
        task_id = input("Enter the ID of the task you want to delete: ")
        found_task = self.find_task_by_id(task_id)
        
        if not found_task:
            print(f"Task with ID '{task_id}' not found.")
            return
        
        # მომხარებლის მხრიდან დავალების წაშლის თანხობის მიღება
        confirmation = input(f"Are you sure you want to delete task '{found_task.description}' (y/n): ").lower()
        if confirmation == 'y':
            self.tasks.remove(found_task)
            self.save_tasks()
            print("Task deleted successfully!")
        else:
            print("Task deletion cancelled.")

    # CSV ფაილში ახალი დავალებების ჩაწერა    
    def save_tasks(self):
        save_tasks_to_csv(self.tasks)

    # CSV ფაილში არსებული დავალებების გადმოტვირთვა tasks ატრიბუტში 
    def load_tasks(self):
        self.tasks = load_tasks_from_csv()

    def run(self): 
        """აპლიკაციის მთავარი ციკლი"""   
        while True:
            print("\nMENU:")
            print("\t1. Create Task")
            print("\t2. Update Task")
            print("\t3. Sort Task")
            print("\t4. View Task")
            print("\t5. Delete Task")
            print("\t6. Exit")
            user_input = input("Enter your command (1-6): ")

            if user_input == '1':
                self.create_task()
            elif user_input == '2':
                self.update_task()
            elif user_input == '3':
                self.sort_task()
            elif user_input == '4':
                self.view_task()
            elif user_input == '5':
                self.delete_task()
            elif user_input == '6':
                print("Exiting To Do List Application.")
                break
            else:
                print("Invalid choice. Please try again.")
