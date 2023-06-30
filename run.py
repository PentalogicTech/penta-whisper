from flask import Flask
from app.routes.task import task_bp
from app.routes.apiCalls import apiCalls_bp



app = Flask(__name__)
app.register_blueprint(task_bp)
app.register_blueprint(apiCalls_bp)




if __name__ == '__main__':
    app.run(debug=True)
