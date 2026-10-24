def validate_register_data(username, password):
    if not username:
        return "Username is required"

    if not password:
        return "Password is required"

    if len(password) < 6:
        return "Password must be at least 6 characters"
      
def validate_login_data(username, password):
    if not username:
        return "Username is required"

    if not password:
        return "Password is required"
      
def validate_task_data(title, description, priority, status, due_date):
    if not title:
        return "Title is required"

    if not due_date:
        return "Due date is required"
      
    valid_priorities = ["High", "Medium", "Low"]

    if priority and priority not in valid_priorities:
        return "Priority must be High, Medium, or Low"
      
    valid_status = ['Pending', 'In Progress', 'Done']
    
    if status and status not in valid_status:
      return "Status must be Pending, In Progress, or Done"
    

def validate_partial_task_data(title, description, priority, status, due_date):
    if all(v is None for v in [title, description, priority, status, due_date]):
        return "At least one field is required"

    if title is not None and not title:
        return "Title cannot be empty"

    if due_date is not None and not due_date:
        return "Due date cannot be empty"

    if priority is not None and priority not in ["High", "Medium", "Low"]:
        return "Priority must be High, Medium, or Low"

    if status is not None and status not in ["Pending", "In Progress", "Done"]:
        return "Status must be Pending, In Progress, or Done"