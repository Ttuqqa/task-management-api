import sqlite3
from config import DB_PATH

#-------------GET CONNECTION-----------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn




#------------ INITIATE TABLES-----------

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    
    
#------------CREATE USER--------
    
def create_user(username, password):
  conn= get_connection()
  cursor= conn.cursor()
  cursor.execute('INSERT INTO users (username,password) VALUES(?,?)',
                 (username,password,))
  
  user_id= cursor.lastrowid
  conn.commit()
  conn.close()
  return user_id

#-------------GET USER BY USERNAME-------------

def get_user_by_username(username):
  conn=get_connection()
  cursor=conn.cursor()
  cursor.execute('SELECT* FROM users WHERE username =?',
                 (username,))
  
  user=cursor.fetchone()
  conn.close()
  return user

#-------------------CREATE TASK------------

def db_create_task(title, description, priority, status,due_date, user_id):
  conn= get_connection()
  cursor=conn.cursor()
  cursor.execute('INSERT INTO tasks (title,description,priority,status,due_date,user_id) VALUES(?,?,?,?,?,?)',
                  (title,description,priority,status,due_date,user_id))
  conn.commit()
  task_id=cursor.lastrowid
  conn.close()
  return task_id

#--------------------DELETE TASK----------------

def db_delete_task(task_id,user_id):
  conn=get_connection()
  cursor=conn.cursor()
  
  cursor.execute('DELETE FROM tasks WHERE id=? AND user_id=?',(task_id,user_id,))
  conn.commit()
  affected=cursor.rowcount
  conn.close()
  return affected

#----------------GET ALL TASKS-----------------

def db_get_all_tasks(user_id, status=None, priority=None, search=None, page=1, limit=10):
  conn=get_connection()
  cursor=conn.cursor()
  query = 'SELECT id,title,description,priority,status,due_date FROM tasks WHERE user_id=?'
  params = [user_id]
  
  if status:
   query += ' AND status=?'
   params.append(status)
   
  if priority:
     query += ' AND priority=?'
     params.append(priority)
     
  if search:
    query += ' AND title LIKE ?'
    params.append(f'%{search}%')
    
  offset = (page - 1) * limit
  query += ' LIMIT ? OFFSET ?'
  params.append(limit)
  params.append(offset)
      
  cursor.execute(query, params)
  
  
  rows= cursor.fetchall()
  conn.close()
  return [{'id' : row[0], 'title': row[1], 'description': row[2],
           'priority': row[3], 'status': row[4], 'due_date':row[5]
           } for row in rows]
  
  
#----------GET ONE TASK------------
def db_get_one_task(task_id,user_id):
  conn=get_connection()
  cursor=conn.cursor()
  cursor.execute('SELECT id,title,description,priority,status,due_date FROM tasks WHERE id=? AND user_id=?',
                 (task_id,user_id,)
                 )
  task= cursor.fetchone()
  
  conn.close()
  
  if task is None:
    return None
  
  return {'id' : task[0], 'title': task[1], 'description': task[2],
           'priority': task[3], 'status': task[4], 'due_date':task[5]
           } 

#-----------UPDATE ALL----------

def db_update_task(title, description, priority, status, due_date, task_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title=?,
            description=?,
            priority=?,
            status=?,
            due_date=?
        WHERE id=? AND user_id=?
    """, (title, description, priority, status, due_date, task_id, user_id))

    conn.commit()

    affected = cursor.rowcount

    conn.close()
    return affected
  