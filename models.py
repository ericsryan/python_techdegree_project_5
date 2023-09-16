from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Title', db.String)
    date = db.Column('Date', db.Date)
    description = db.Column('Description', db.Text)
    skills = db.Column('Skills', db.Text)
    repo_link = db.Column('Link', db.Text)

    def __repr__(self):
        return f"""<Project Title: {self.title} Date Completed: {self.date}>"""