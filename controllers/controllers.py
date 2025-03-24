from datetime import datetime
from flask import request, render_template , flash
from flask import current_app as app
from models.models import *
from models.database import db


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uName = request.form.get('username')
        pWord = request.form.get('password')
        user = User.query.filter_by(username=uName , password = pWord).first()
        if user and user.id == 1:
            return render_template('admin_dashboard.html')
        elif user:
            return render_template('user_dashboard.html')
        else:
            flash('User not found')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uName = request.form.get('username')
        pWord = request.form.get('password')
        fName = request.form.get('full_name')
        qualificaton = request.form.get('qualification')
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        user = User.query.filter_by(username=uName).first()
        if user:
            flash('User already exists')
            return render_template('login.html')
        else:
            print(request.form) 
            new_user = User(username=uName, password = pWord , full_name = fName , qualification = qualificaton , dob = dob)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully', 'success')
            return render_template('login.html')
    return render_template('register.html')

def admin_dashboard():
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', subjects=subjects)

