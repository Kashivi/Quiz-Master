from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(60) , nullable = False , unique = True)
    password = db.Column(db.Text , nullable = False)
    full_name = db.Column(db.String(80) , nullable = False)
    qualification = db.Column(db.String(30) , nullable = False)
    dob = db.Column(db.Date , nullable = False)
    scores = db.relationship("Score", backref = "user", lazy = True , cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False , unique = True)
    description = db.Column(db.String(500) , nullable = False)
    chapters = db.relationship("Chapter", backref = "subject", lazy = True , cascade="all, delete-orphan")


class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    description = db.Column(db.String(500) , nullable = False)
    subject_id = db.Column(db.Integer , db.ForeignKey('subject.id') , nullable = False)
    quizzes = db.relationship("Quiz", backref = "chapter", lazy = True , cascade="all, delete-orphan")

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer , primary_key = True)
    chapter_id = db.Column(db.Integer , db.ForeignKey('chapter.id') , nullable = False)
    date_of_quiz = db.Column(db.DateTime , nullable = False)
    time_duration = db.Column(db.String(5) , nullable = False)
    remarks = db.Column(db.String(500) , nullable = True)

    questions = db.relationship('Question', backref='quiz', lazy=True , cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True , cascade="all, delete-orphan")

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer , primary_key = True)
    quiz_id = db.Column(db.Integer , db.ForeignKey('quiz.id') , nullable = False)
    question_statement = db.Column(db.String(500) , nullable = False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    
class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer , primary_key = True)
    quiz_id = db.Column(db.Integer , db.ForeignKey('quiz.id') , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    attempt_number = db.Column(db.Integer, nullable = False, default = 0) 
    time_stamp_of_attempt = db.Column(db.DateTime ,  default = datetime.utcnow)
    total_scored = db.Column(db.Integer , default = 0)
    total_possible_score = db.Column(db.Integer, nullable = False)
    __table_args__ = (db.UniqueConstraint('quiz_id', 'user_id', 'attempt_number', name='unique_attempt'),)