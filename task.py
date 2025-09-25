class Task :

    last_task_id = 0
    
    def __init__(self, title:str, description:str, priority:str = "P1", status:str = "Doing") :
        self.id = Task.last_task_id + 1
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        Task.last_task_id += 1
