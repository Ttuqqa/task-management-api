from flask import Flask

from database.db import init_db
from routes.user_routes import user_bp
from routes.task_routes import task_bp
from utils.error_handler import register_error_handlers


app=Flask(__name__)



init_db()

register_error_handlers(app)

app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

@app.route("/")
def home():
  return{'message':"task managment api is running"}

if __name__== "__main__":
  app.run(debug=True)
  