from flask import g
from database.db import db_delete_task,db_create_task, db_get_all_tasks, db_get_one_task,db_update_task
from utils.response import success_response,error_response

#-------CREATE TASK-------

def create_task(title, description, priority, status, due_date):
  user_id= g.user['user_id']
  
  priority = priority if priority else 'Medium'
  status = status if status else 'Pending'
  
  task_id=db_create_task(
        title,
        description,
        priority,
        status,
        due_date,
        user_id
    )

 
  return success_response("Task created successfully",
        {"task_id": task_id}, status_code=201)
  
#------------DELETE TASK-------------

def delete_task(task_id):
  user_id=g.user['user_id']
  
  if not task_id :
    return error_response('Validation failed',
                          'task_id is required',
                          status_code=400
                          )
  
  affected= db_delete_task(task_id,user_id)
  
  if affected==0:
   return error_response(
    "Delete failed",
    "Task not found or access denied",
    status_code= 404
)  
  return success_response('Task deleted successfully')

#------------GET ALL TASKS------------

def get_all_tasks(status=None, priority=None, search=None, page=1, limit=10):
  user_id= g.user['user_id']
  tasks=db_get_all_tasks(user_id,status,priority,search,page,limit)
  return success_response('Tasks retrived successfully', tasks)

#------------ GET ONE TASK --------------------

def get_one_task(task_id):
  user_id=g.user['user_id']
  
  if not task_id :
    return error_response('Validation failed',
                          'task_id is required',
                          status_code=400
                          )
  
  task=db_get_one_task(task_id, user_id)
  
  if not task:
    return error_response(
        "Task not found",
        "Task not found or access denied",
        status_code=404
    )
    
  return success_response('Task retrived successfully',task)
  
#----------UPDATE-----------

def update_task(task_id, title, description, priority, status, due_date):
    user_id = g.user['user_id']

    priority = priority if priority else 'Medium'
    status = status if status else 'Pending'

    affected = db_update_task(
        title,
        description,
        priority,
        status,
        due_date,
        task_id,
        user_id
    )

    if affected == 0:
        return error_response("Update failed", "Task not found", status_code=404)

    return success_response(
        "Task updated successfully",
        {"task_id": task_id}
    )
    
#------------ PARTIAL UPDATE-----------

def partial_update_task(task_id, title, description, priority, status, due_date):
    user_id = g.user["user_id"]

    
    task = db_get_one_task(task_id, user_id)

    
    if task is None:
        return error_response(
            "Task not found",
            "Task not found or access denied",
            status_code=404
        )

    
    if title is None:
        title = task["title"]

    if description is None:
        description = task["description"]

    if priority is None:
        priority = task["priority"]

    if status is None:
        status = task["status"]

    if due_date is None:
        due_date = task["due_date"]

    
    affected = db_update_task(
        title,
        description,
        priority,
        status,
        due_date,
        task_id,
        user_id
    )

    
    if affected == 0:
        return error_response(
            "Update failed",
            "No rows updated",
            status_code=500
        )

    return success_response("Task updated successfully")