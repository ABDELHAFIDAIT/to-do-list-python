from db import engine, tasks
from task import Task
from sqlalchemy import insert, select, delete

class TaskManager() :
    
    def __init__(self, engine, table) :
        self.engine = engine
        self.table = table
    
    
    def add(self, task:Task) :
        with self.engine.begin() as conn :
            try :
                conn.execute(
                    insert(self.table)
                    .values(
                        title = task.title,
                        description = task.description,
                        priority = task.priority,
                        status = task.status
                    )
                )
                print("Task Added Successfully !")
            except Exception as e :
                print("Error : \n", e)
    
    
    def index(self) :
        with self.engine.begin() as conn :
            try :
                stmt = select(self.table)
                result = conn.execute(stmt)
                rows = result.fetchall()
                return rows
            except Exception as e :
                print("Error : \n", e)
    

    def show(self, id) :
        with self.engine.begin() as conn :
            try :
                stmt = select(self.table).where(self.table.c.id == id)
                result = conn.execute(stmt)
                rows = result.fetchall()
                if len(rows) > 0 :
                    return rows
                else :
                    return "ID Not Found !"
            except Exception as e :
                print("Error : \n", e)


    def delete(self, id:int) :
        with self.engine.begin() as conn :
            try :
                stmt = delete(self.table).where(self.table.c.id == id)
                conn.execute(stmt)
                print("Task Deleted Successfully !")
            except Exception as e :
                print("Error : \n", e)