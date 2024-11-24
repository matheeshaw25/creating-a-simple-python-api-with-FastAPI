from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4 # unique identifier

app = FastAPI()

#pydantic model
class Task(BaseModel):
    id : Optional[UUID] = None
    title : str
    description : Optional[str] = None
    completed : bool = False


tasks = []

@app.post("/tasks/", response_model=Task) # use Task model
def create_task(task: Task): # create new task using Pydantic model
    task.id = uuid4()
    tasks.append(task) # append info to tasks list
    return task
    

@app.get("/tasks/", response_model=List[Task]) # 
def read_tasks():
    return tasks


# Run the API
if __name__ == "__main__":
    import uvicorn # webserver that allows  to run api

    uvicorn.run(app, host="0.0.0.0", port=8000) # 0.0.0.0 local ip adress
