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

    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relacionamento com JobSearch e UserActivity
    job_searches = db.relationship('JobSearch', backref='user', lazy=True)
    activities = db.relationship('UserActivity', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class JobSearch(db.Model):
    __tablename__ = 'job_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    search_term = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f"<JobSearch {self.search_term} by User {self.user_id}>"

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    activity_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())
    details = db.Column(db.Text)

    def __repr__(self):
        return f"<UserActivity {self.activity_type} by User {self.user_id}>"
