from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def nairobi_time():
    return datetime.now(pytz.timezone('Africa/Nairobi'))
    return datetime.now(timezone)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.id}>'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')

        if task_content:
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                return f"There was an issue adding your task: {e}"
        else:
            return "Task content cannot be empty"

    else:
        tasks = Todo.query.order_by(Todo.id.asc()).all()
        return render_template("index.html", tasks=tasks)


# Optional: Delete task route
@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"There was a problem deleting that task: {e}"

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an issue updating the task: {e}"

    else:
        return render_template('edit.html', task=task)



if __name__ == '__main__':
    app.run(debug=True)
