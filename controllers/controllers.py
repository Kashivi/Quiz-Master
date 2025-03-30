from datetime import datetime
from flask import request, render_template , flash , redirect, url_for
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
            return redirect(url_for('admin_dashboard'))
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

@app.route('/admin_dashboard')
def admin_dashboard():

    subjects = Subject.query.all()
    for subject in subjects:
        for chapter in subject.chapters:
            chapter.questionCount = Question.query.filter_by(chapter_id=chapter.id).count()
    return render_template('admin_dashboard.html', subjects=subjects)


@app.route('/admin_dashboard/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        subject = Subject.query.filter_by(name=name).first()
        if subject:
            flash('Subject already exists')
            return redirect(url_for('admin_dashboard'))
        else:
            new_subject = Subject(name=name, description=description)
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('add_subject.html')


@app.route('/admin_dashboard/add_chapter/<int:subject_id>', methods=['GET', 'POST'])
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        chapter = Chapter.query.filter_by(name=name, subject_id=subject_id).first()
        if chapter:
            flash('Chapter already exists')
            return redirect(url_for('admin_dashboard'))
        else:
            new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash('Chapter added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('add_chapter.html', subject=subject)


@app.route('/admin_dashboard/delete-subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    db.session.delete(subject)
    db.session.commit()

    flash("Subject deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id) 
    if request.method == 'POST':
        subject.name = request.form.get('name')
        subject.description = request.form.get('description')
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_subject.html', subject=subject)


@app.route('/quiz_management/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        db.session.commit()
        flash('Chapter updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_chapter.html', chapter=chapter)

@app.route('/quiz_management/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/quiz-management')
def quiz_management():
    quizzes = Quiz.query.all()
    return render_template('quiz_management.html', quizzes=quizzes)  

@app.route('/quiz_management/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        name = request.form.get('name')
        chapter_id = request.form.get('chapter_id')
        subject_id = request.form.get('subject_id')
        date_of_quiz = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')

        try:
            date_of_quiz = datetime.strptime(date_of_quiz, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format", "danger")
            return redirect(url_for('add_quiz'))

        new_quiz = Quiz(
            name=name,
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            subject_id=subject_id, 
            time_duration=time_duration,
            remarks=remarks
        )

        db.session.add(new_quiz)
        db.session.commit()

        flash("Quiz added successfully!", "success")
        return redirect(url_for('quiz_management'))

    chapters = Chapter.query.all()
    subjects = Subject.query.all() 
    return render_template('add_quiz.html', chapters=chapters, subjects=subjects)

@app.route('/quiz_management/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.q_title = request.form.get('q_title')
        question.question_statement = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        question.correct_option = request.form.get('correct_option')
        db.session.commit()
        flash('Question updated!', 'success')
        return redirect(url_for('quiz_management'))
    return render_template('edit_question.html', question=question)

@app.route('/quiz_management/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted!', 'success')
    return redirect(url_for('quiz_management'))

@app.route('/quiz_management/add_question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        # Get form data
        q_title = request.form.get('q_title')
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        # Validate correct_option (Ensure it's between 1 and 4)
        try:
            correct_option = int(correct_option)
            if correct_option not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            flash("Invalid correct option! Choose a number between 1 and 4.", "danger")
            return redirect(url_for('add_question', quiz_id=quiz_id))

        # Get chapter ID from the quiz
        chapter_id = quiz.chapter_id  

        # Get next available question number
        last_question = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id.desc()).first()
        question_number = 1 if last_question is None else last_question.id + 1  

        # Create new question
        new_question = Question(
            q_title=q_title,
            chapter_id=chapter_id,
            quiz_id=quiz_id,
            question_statement=question_statement,
            question_number=question_number,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )

        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!', 'success')

        # Redirect to the question list for the quiz
        return redirect(url_for('quiz_management'))  # Change this if you have a separate question list page
    
    return render_template('add_question.html', quiz=quiz)


@app.route('/quiz_management/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch quiz by ID
    chapters = Chapter.query.all()  # Fetch all chapters

    if request.method == 'POST':
        new_chapter_id = request.form['chapter_id']  # Get new chapter ID from form

        # Update the quiz
        quiz.chapter_id = new_chapter_id
        db.session.commit()

        # Update all related questions (optional: only if necessary)
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        for question in questions:
            question.chapter_id = new_chapter_id  # Update chapter reference in questions
        db.session.commit()

        flash("Quiz and its questions updated successfully!", "success")
        return redirect(url_for('quiz_management'))

    return render_template('edit_quiz.html', quiz=quiz, chapters=chapters)  # Pass chapters

@app.route('/quiz_management/delete-quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch quiz by ID

    # Delete the quiz and related questions & scores (cascade delete is set)
    db.session.delete(quiz)
    db.session.commit()

    flash("Quiz deleted successfully!", "success")
    return redirect(url_for('quiz_management'))




