from datetime import datetime

# დავალების ობიექტის შექმნა შესაბამისი ატრიბუტებითა და მეთოდებით
class Task:
    def __init__(self,description):
        self.task_id = ""
        self.__create_date = datetime.now()
        self.description = description
        self.priority = None
        self.status = None

    # დავალების პრიორიტეტის დადგენის მეთოდი   
    def set_priority(self,priority_id):
        if priority_id == '1':
            self.priority = "low"
        elif priority_id == '2':
            self.priority ="Medium"
        elif priority_id == '3':
            self.priority ="High"
        elif priority_id == '4':
            self.priority ="Critical"
        else:
            print("wrong priority number!")

    # დავალების სტატუსის დადგენის მეთოდი 
    def set_status(self,status_id):
        if status_id == '1':
            self.status = "Not Started"
        elif status_id == '2':
            self.status ="Working on it"
        elif status_id == '3':
            self.status ="Stuck"
        elif status_id == '4':
            self.status ="Done"
        else:
            print("wrong status number!")
# დავალება.ობიექტი, დაწყება-დასრულების ატრიბუტებით  
class StartDateDueDateTask(Task):
    def __init__(self, description, start_date,due_date):
        super().__init__(description)
        self.start_date = start_date
        self.due_date = due_date