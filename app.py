from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key = True)
    ToDo_Title = db.Column(db.String(100), nullable=False)
    ToDo_Description = db.Column(db.String(300))
    Date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.ToDo_Title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print("POST request detected!")
        # Get data from the form
        title = request.form.get('title') 
        description = request.form.get('description')
        
        # Create a new Todo entry
        new_todo = Todo(ToDo_Title=title, ToDo_Description=description)
        db.session.add(new_todo)
        db.session.commit()

    # Fetch all todos (for both GET and POST)
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is products page."

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
def update(SNo):
    if request.method == 'POST':
        title = request.form.get('title') 
        description = request.form.get('description')
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.ToDo_Title = title
        todo.ToDo_Description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=True)  