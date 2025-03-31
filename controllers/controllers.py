from datetime import datetime , timedelta
from flask import request, render_template , flash , redirect, url_for , session
from flask import current_app as app
from models.models import *
from sqlalchemy.sql import func
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
        session['user_id'] = user.id 

        if user and user.id == 1:
            return redirect(url_for('admin_dashboard'))
        elif user:
            return redirect(url_for('user_dashboard'))
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

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login')) 

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
        q_title = request.form.get('q_title')
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')
        try:
            correct_option = int(correct_option)
            if correct_option not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            flash("Invalid correct option! Choose a number between 1 and 4.", "danger")
            return redirect(url_for('add_question', quiz_id=quiz_id))
        chapter_id = quiz.chapter_id  
        last_question = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id.desc()).first()
        question_number = 1 if last_question is None else last_question.id + 1  
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
        return redirect(url_for('quiz_management')) 
    
    return render_template('add_question.html', quiz=quiz)


@app.route('/quiz_management/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id) 
    chapters = Chapter.query.all()  

    if request.method == 'POST':
        quiz.name = request.form.get('name')  # Update Quiz Name
        quiz.chapter_id = request.form.get('chapter_id')  # Update Chapter
        quiz.date_of_quiz = datetime.strptime(request.form.get('date_of_quiz'), "%Y-%m-%d").date() # Update Date
        time_duration = request.form.get('time_duration')
        if time_duration:
            try:
                quiz.time_duration = int(time_duration)
            except ValueError:
                flash("Invalid time duration! Please enter a number.", "danger")
                return redirect(url_for('edit_quiz', quiz_id=quiz_id))

        quiz.remarks = request.form.get('remarks')

        db.session.commit() 

        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        for question in questions:
            question.chapter_id = quiz.chapter_id  # Update chapter ID for questions

        db.session.commit()  # Save questions update

        flash("Quiz and its questions updated successfully!", "success")
        return redirect(url_for('quiz_management'))

    return render_template('edit_quiz.html', quiz=quiz, chapters=chapters)


@app.route('/quiz_management/delete-quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id) 
    db.session.delete(quiz)
    db.session.commit()

    flash("Quiz deleted successfully!", "success")
    return redirect(url_for('quiz_management'))

@app.route('/user_dashboard')
def user_dashboard():
    
    current_user = User.query.get(session['user_id'])

    total_quizzes = Quiz.query.count()
    completed_quizzes = db.session.query(Score.quiz_id).filter_by(user_id=current_user.id).distinct().count()

    user_scores = [score.total_scored for score in current_user.scores]
    
    # Get upcoming quizzes (quizzes that haven't happened yet)
    upcoming_quizzes = Quiz.query.filter(Quiz.date_of_quiz > datetime.utcnow()).all()
    
    return render_template('user_dashboard.html',
                         user=current_user,
                         quizzes=upcoming_quizzes,
                         total_quizzes=total_quizzes,
                         completed_quizzes=completed_quizzes,
                         user_id=current_user.id)

@app.route('/user_dashboard/quiz_details/<int:quiz_id>')
def quiz_details(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz_details.html', quiz=quiz)

@app.route('/user_dashboard/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('login'))

    quiz = Quiz.query.get_or_404(quiz_id)

    # Get the current time
    current_time = datetime.utcnow()
    quiz_start_time = quiz.date_of_quiz
    quiz_end_time = quiz_start_time + timedelta(minutes=int(quiz.time_duration))  # End time

    if current_time < quiz_start_time:
        flash("⏳ The quiz has not started yet!", "warning")
        return redirect(url_for('user_dashboard'))

    if current_time > quiz_end_time:
        flash("The quiz time is over!", "danger")
        return redirect(url_for('user_dashboard'))

    session['quiz_start_time'] = current_time.timestamp()
    duration_seconds = int(quiz.time_duration) * 60
    end_time = current_time.timestamp() + duration_seconds

    # Get all questions
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if not questions:
        flash("⚠️ No questions available for this quiz!", "danger")
        return redirect(url_for('user_dashboard'))

    return render_template(
        'quiz_interface.html',
        quiz=quiz,
        question=questions[0],
        question_num=1,
        total_questions=len(questions),
        end_time=int(end_time * 1000)  
    )



@app.route('/save_answer', methods=['POST'])
def save_answer():
    user_id = session.get('user_id')


    quiz_id = request.form.get('quiz_id')
    question_id = request.form.get('question_id')
    selected_option = request.form.get('selected_option')
    action = request.form.get('action')  # "next" or "submit"

    if not all([quiz_id, question_id, selected_option]):
        flash("Invalid submission!", "danger")
        return redirect(url_for('user_dashboard'))

    quiz_id, question_id, selected_option = int(quiz_id), int(question_id), int(selected_option)
    existing_answer = Answer.query.filter_by(user_id=user_id, quiz_id=quiz_id, question_id=question_id).first()

    if existing_answer:
        print("🔄 Updating existing answer")
        existing_answer.selected_option = selected_option
    else:
        print("➕ Saving new answer")
        new_answer = Answer(user_id=user_id, quiz_id=quiz_id, question_id=question_id, selected_option=selected_option)
        db.session.add(new_answer)

    try:
        db.session.commit()
        print("✅ Answer successfully saved!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR: Failed to save answer! Reason: {e}")
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_ids = [q.id for q in questions]

    current_index = question_ids.index(question_id)
    next_index = current_index + 1

    if action == "submit" or next_index >= len(questions):
        return redirect(url_for('calculate_score', quiz_id=quiz_id))  # Redirect to score calculation
    
    next_question_id = question_ids[next_index]
    return redirect(url_for('quiz_interface', quiz_id=quiz_id, question_id=next_question_id))


@app.route('/user_dashboard/quiz_results/<int:quiz_id>')
def quiz_results(quiz_id):
    quiz = Quiz.query.get(quiz_id)  # Get the quiz
    user_id = session.get('user_id')  # Get logged-in user ID

    if not quiz:
        return "Quiz not found!", 404

    # Check if the user has attempted this quiz
    score = Score.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()

    if not score:  # If no score exists, redirect to quiz start page
        flash("You haven't attempted this quiz yet! Redirecting...", "warning")
        return redirect(url_for("quiz_interface", quiz_id=quiz_id))

    # Calculate percentage
    total_questions = len(quiz.questions) 
    percentage = (score.total_scored / total_questions) * 100 if total_questions > 0 else 0

    return render_template(
        "quiz_results.html",
        quiz=quiz,
        score=score.total_scored,
        total_questions=total_questions,
        percentage=round(percentage, 2)
    )



@app.route('/user_dashboard/submit_quiz/<int:quiz_id>', methods=['GET'])
def submit_quiz(quiz_id):
    print(f"✅ DEBUG: Submitting Quiz ID={quiz_id}")

    user_id = session.get('user_id')

    user_answers = Answer.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()

    if not user_answers:
        return redirect(url_for('user_dashboard'))

    # Calculate score
    total_correct = 0
    total_questions = len(user_answers)

    for answer in user_answers:
        correct_option = Question.query.get(answer.question_id).correct_option
        if answer.selected_option == correct_option:
            total_correct += 1

        last_attempt = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id) \
            .order_by(Score.attempt_number.desc()).first()

        attempt_number = last_attempt.attempt_number + 1 if last_attempt else 1

        score_entry = Score(user_id=user_id, quiz_id=quiz_id, total_scored=total_correct, total_possible_score=total_questions, attempt_number=attempt_number)
        db.session.add(score_entry)


 
    db.session.commit()
    print(f"✅ Quiz submitted! Score: {total_correct}/{total_questions}")
   
    session.pop('quiz_start_time', None)

    return redirect(url_for('quiz_results', quiz_id=quiz_id))




@app.route('/calculate_score/<int:quiz_id>')
def calculate_score(quiz_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('login'))

    print(f"📊 DEBUG: Calculating score for User={user_id}, Quiz={quiz_id}")

    # ✅ Fetch all answers
    user_answers = Answer.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()

    if not user_answers:
        print("❌ ERROR: No answers found for this quiz!")
        flash("No answers found!", "danger")
        return redirect(url_for('user_dashboard'))

    total_questions = len(user_answers)
    correct_answers = db.session.query(func.count(Answer.id)) \
    .join(Question, Answer.question_id == Question.id) \
    .filter(
        Answer.user_id == user_id,
        Answer.quiz_id == quiz_id,
        Answer.selected_option == Question.correct_option
    ).scalar()


    # ✅ Find last attempt number (if exists)
    last_attempt = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).order_by(Score.attempt_number.desc()).first()
    attempt_number = last_attempt.attempt_number + 1 if last_attempt else 1

    # ✅ Save Score in DB
    new_score = Score(
        user_id=user_id,
        quiz_id=quiz_id,
        total_scored=correct_answers,
        total_possible_score=total_questions,
        attempt_number=attempt_number
    )
    db.session.add(new_score)

    try:
        db.session.commit()
        print(f"✅ DEBUG: Score saved! Attempt {attempt_number}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR: Failed to save score! Reason: {e}")

    return redirect(url_for('quiz_results', quiz_id=quiz_id))


@app.route('/quiz_interface/<int:quiz_id>/<int:question_id>')
def quiz_interface(quiz_id, question_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('login'))

    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    # ✅ Get the stored start time
    if 'quiz_start_time' not in session:
        flash("Session expired! Restarting quiz.", "warning")
        return redirect(url_for('start_quiz', quiz_id=quiz_id))

    start_time = session['quiz_start_time']
    end_time = start_time + (int(quiz.time_duration) * 60)  # Convert to int before multiplication
    end_timestamp = int(end_time * 1000)  # Convert to milliseconds

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_ids = [q.id for q in questions]
    total_questions = len(questions)
    question_num = question_ids.index(question_id) + 1  

    return render_template("quiz_interface.html",
                           quiz=quiz,
                           question=question,
                           question_num=question_num,
                           total_questions=total_questions,
                           end_time=end_timestamp)


@app.route('/quiz_summary')
def quiz_summary():
    # Query to aggregate quiz summary per user
    summary_query = (
        db.session.query(
            User.full_name.label("user_name"),
            Quiz.name.label("quiz_name"),
            Chapter.name.label("chapter_name"), 
            func.count(Score.attempt_number).label("total_attempts"),
            func.max(Score.total_scored).label("best_score"),
            func.avg(Score.total_scored).label("average_score"),
            func.max(Score.total_possible_score).label("total_possible_score")
        )
        .join(Score, User.id == Score.user_id)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .group_by(User.id, Quiz.id, Chapter.id)
        .all()
    )

    return render_template("quiz_summary.html", summary=summary_query)

@app.route('/quiz_score/<int:user_id>')
def quiz_score(user_id):
    # Get the user (optional, for debugging or display)
    user = User.query.get(user_id)
    
    # Get all quizzes for the user (first attempt only)
    user_quizzes = db.session.query(Quiz.id, Quiz.name) \
        .join(Score, Score.quiz_id == Quiz.id) \
        .filter(Score.user_id == user_id, Score.attempt_number == 1) \
        .all()

    quiz_scores = []
    for quiz in user_quizzes:
        quiz_id = quiz.id
        quiz_name = quiz.name
        
        # Get the score and timestamp of the first attempt for each quiz
        first_attempt_scores = db.session.query(Score.total_scored, Score.time_stamp_of_attempt) \
            .filter_by(user_id=user_id, quiz_id=quiz_id) \
            .order_by(Score.attempt_number.desc()) \
            .first()


        # Get the answers for the first attempt of each quiz
        first_attempt_answers = db.session.query(
            Answer.selected_option,
            (Answer.selected_option == Question.correct_option).label('is_correct')
        ) \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user_id == user_id, Answer.quiz_id == quiz_id) \
        .all()

        quiz_scores.append({
            'quiz_name': quiz_name,
            'score': first_attempt_scores.total_scored if first_attempt_scores else 0,
            'date_of_attempt': first_attempt_scores.time_stamp_of_attempt if first_attempt_scores else None,
            'answers': first_attempt_answers
        })

    return render_template("quiz_score.html", 
                           user=user, 
                           quiz_scores=quiz_scores)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('user_dashboard'))  # Redirect to the dashboard or wherever appropriate

    # Search for quizzes by name
    quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
    
    # Search for subjects by name
    subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()

    # If you want to find quizzes related to the subjects found
    for subject in subjects:
        related_quizzes = Quiz.query.filter(Quiz.subject_id == subject.id).all()
        quizzes.extend(related_quizzes)

    # Remove duplicates if any
    quizzes = list({quiz.id: quiz for quiz in quizzes}.values())

    return render_template('search_results.html', quizzes=quizzes, subjects=subjects, query=query)

@app.route('/admin/search', methods=['GET'])
def admin_search():
    query = request.args.get('query', '').strip()
    
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('admin_dashboard'))

    # Search for users
    users = User.query.filter(User.full_name.ilike(f'%{query}%')).all()

    # Search for subjects
    subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()

    # Search for quizzes
    quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()

    # Search for questions
    questions = Question.query.filter(Question.q_title.ilike(f'%{query}%')).all()

    return render_template('admin_search.html', users=users, subjects=subjects, quizzes=quizzes, questions=questions, query=query)

