# File: To-Do-App/app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.title} - {self.desc} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

# Ensure tables are created only once
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))  # Prevent re-submission on refresh
    all_todos = Todo.query.all()
    return render_template("index.html", all_todos=all_todos)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:SNo>', methods=['GET', 'POST'])
def edit(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/shows')
def shows():
    all_todos = Todo.query.all()
    return f"All Todos: {all_todos}"

if __name__ == "__main__":
    app.run(debug=True)
