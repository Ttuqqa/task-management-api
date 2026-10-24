from flask import Blueprint, request
from services.task_service import create_task, delete_task, get_all_tasks, get_one_task,update_task,partial_update_task
from utils.validation import validate_task_data, validate_partial_task_data
from utils.response import error_response
from utils.auth import token_required

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['POST'])
@token_required
def add_task():
    data = request.get_json()
    
    error = validate_task_data(
    data.get("title"),
    data.get("description"),
    data.get("priority"),
    data.get("status"),
    data.get("due_date")
)
    if error:
      return error_response(error,status_code=400)
    
    result = create_task(
        data.get("title"),
        data.get("description"),
        data.get("priority"),
        data.get("status"),
        data.get("due_date")
    )
    

    return result
  
#--------DELETE----------
  
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def remove_task(task_id):
  
  return delete_task(task_id)


#-------GET ALL--------

@task_bp.route('/tasks', methods=['GET'])
@token_required
def getall_tasks():
  status = request.args.get("status")
  priority = request.args.get("priority")
  search = request.args.get("search")
  page = request.args.get("page", 1, type=int)
  limit = request.args.get("limit", 10, type=int)
  page = max(page, 1)
  limit = max(1, min(limit, 50))

  return get_all_tasks(status, priority, search, page, limit)
#------- GET ONE TASK--------

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def getone_task(task_id):
  return get_one_task(task_id)

#---------UPDATE------------
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task_route(task_id):
    data = request.get_json()
    error = validate_task_data(
        data.get("title"),
        data.get("description"),
        data.get("priority"),
        data.get("status"),
        data.get("due_date")
    )

    if error:
        return error_response(error, status_code=400)

    return update_task(
    task_id,
    data.get("title"),
    data.get("description"),
    data.get("priority"),
    data.get("status"),
    data.get("due_date")
)
  
#---------PATCH UPDATE----------

@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
@token_required
def partialupdate_route(task_id):
  data = request.get_json()
  
  error = validate_partial_task_data(
        data.get("title"),
        data.get("description"),
        data.get("priority"),
        data.get("status"),
        data.get("due_date")
    )

  if error:
      return error_response(error, status_code=400)

  return partial_update_task(
    task_id,
    data.get("title"),
    data.get("description"),
    data.get("priority"),
    data.get("status"),
    data.get("due_date")
   )
