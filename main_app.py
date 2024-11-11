import os

from dotenv import load_dotenv
from flask import Flask

from models import init_db
from student_route import student_router

app = Flask(__name__)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "Secret_Key-2024")
app.config["SECRET_KEY"] = SECRET_KEY

with app.app_context():
    init_db()

app.register_blueprint(student_router)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
