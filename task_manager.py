from db import engine, tasks
from sqlalchemy import *

class TaskManager() :
    
    def __init__(self, engine, table) :
        self.engine = engine
        self.table = table
    
    
    def store(self, title, description, priority, status):
        with self.engine.begin() as conn:
            try:
                if not title.strip():
                    return "Task's Title Cannot be Empty!"
                elif not description.strip():
                    return "Task's Description Cannot be Empty!"
                conn.execute(
                    insert(self.table).values(
                        title=title,
                        description=description,
                        priority=priority,
                        status=status
                    )
                )
                return "Task Added Successfully!"
            except Exception as e:
                return f"Error: {e}"
    
    
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