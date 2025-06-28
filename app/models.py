from datetime import datetime
from app import db

    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))     
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.email}>'
 
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))     
    description = db.Column(db.Text) 
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
 
class Enrollment(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    student_id = db.Column(db.Integer, db.ForeignKey('student.id')) 
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
 
 