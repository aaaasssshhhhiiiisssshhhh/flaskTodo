from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['todo']
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')


@app.route('/update', methods=['POST'])
def update_todo():
    todo_id = request.form['todo_id']
    new_task = request.form['new_task']
    todo = Todo.query.get(todo_id)
    todo.task = new_task
    db.session.commit()
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete_todo():
    todo_id = request.form['todo']
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
