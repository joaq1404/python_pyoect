#import
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#db connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
#table create
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        title = request.json['title']
        description = request.json['description']
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit() 
        return task_schema.jsonify(new_task), 201  
    except Exception as e:
        print("Error:", e)
        return "Error processing request", 400

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)  
    
    if not task: 
        return jsonify({'message': 'Task not found'}), 404  
    try:
        
        title = request.json['title']
        description = request.json['description']
        task.title = title
        task.description = description
        db.session.commit()
        
        return task_schema.jsonify(task) 
    except Exception as e:
        print("Error:", e)
        return "Error updating task", 500  



@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    try:
        db.session.delete(task)  
        db.session.commit() 
        
        return task_schema.jsonify(task)  
    except Exception as e:
        print("Error:", e)
        return "Error deleting task", 500  


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
