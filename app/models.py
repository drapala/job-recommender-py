from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    requirements = db.Column(db.Text)
    salary = db.Column(db.Float)
