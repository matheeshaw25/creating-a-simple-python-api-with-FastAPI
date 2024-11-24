from fastapi import FastAPI, HTTPException
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


@app.get("/tasks/{task_id}", response_model=Task) 
def read_task(task_id: UUID):
    for task in tasks: #check each task in list with id passed
        if task.id == task_id:
            return task
    
    return HTTPException(status_code=404, detail="Task not found") #if task not there

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
        
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model= Task)
def delete_task(task_id : UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(idx)
            return deleted_task
        
    raise HTTPException(status_code=404, detail="Task not found")


# Run the API
if __name__ == "__main__":
    import uvicorn # webserver that allows  to run api

    uvicorn.run(app, host="0.0.0.0", port=8000) # 0.0.0.0 local ip adress
