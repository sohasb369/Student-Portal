from flask import Blueprint, current_app, jsonify, request, session, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Student, Course, Enrollment
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def app_academy_dashboard():
    recent_courses = Course.query.order_by(Course.id.desc()).limit(3).all()
    
    if 'email' in session:
        return render_template("app_academy_dashboard.html", 
                            logged_in=True,
                            recent_courses=recent_courses)
    return render_template('app_academy_dashboard.html',
                         recent_courses=recent_courses)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('main.login'))
        
        student = Student.query.filter_by(email=email).first()
        
        if not student or not check_password_hash(student.password, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.login'))
        
        session['email'] = email
        session['logged_in'] = True
        
        flash('Logged in successfully!', 'success')
        
        redirect_url = request.args.get('redirect')
        if redirect_url:
            return redirect(redirect_url)
        return redirect(url_for('main.app_academy_dashboard'))
    
    return render_template("login.html")

@main_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('main.signup'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('main.signup'))
        
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash('Email already exists!', 'error')
            return redirect(url_for('main.signup'))

        new_student = Student(
            email=email,
            password=generate_password_hash(password),
            authenticated=False
        )
        db.session.add(new_student)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template("signup.html")



@main_bp.route('/app_student_list')
def app_student_list():
    enrollments = db.session.query(
        Enrollment,
        Student,
        Course
    ).join(
        Student, Enrollment.student_id == Student.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).all()
    
    students_data = {}
    for enrollment, student, course in enrollments:
        if student.email not in students_data:
            students_data[student.email] = {
                'student': student,
                'courses': []
            }
        students_data[student.email]['courses'].append(course)
    
    return render_template('app_student_list.html', students_data=students_data)

@main_bp.route('/pages_profile_student')
def pages_profile_student():
    if 'email' not in session:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('main.login'))
    
    student = Student.query.filter_by(email=session['email']).first()
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('main.login'))
    
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    enrolled_courses = [enrollment.course for enrollment in enrollments]
    
    return render_template('pages_profile_student.html', 
                         student=student,
                         enrolled_courses=enrolled_courses)

@main_bp.route('/add-courses')
def add_courses():
    try:
        courses_data = [
            {"title": "Basics of Angular", "description": "The material of this course is also covered in my other course about web design and development with HTML5 & CSS3. Scroll to the bottom of this page to check out that course, too! If you're already taking my other course, you already have all it takes to start designing beautiful websites today!"},
            {"title": "Python Fundamentals", "description": "Learn Python programming from scratch.The material of this course is also covered in my other course about web design and development with HTML5 & CSS3. Scroll to the bottom of this page to check out that course, too! If you're already taking my other course, you already have all it takes to start designing beautiful websites today!"},
            {"title": "Web Design Principles", "description": "Master the fundamentals of UI/UX design.The material of this course is also covered in my other course about web design and development with HTML5 & CSS3. Scroll to the bottom of this page to check out that course, too! If you're already taking my other course, you already have all it takes to start designing beautiful websites today!"}
        ]
        
        for data in courses_data:
            if not Course.query.filter_by(title=data['title']).first():
                new_course = Course(
                    title=data['title'],
                    description=data['description']
                )
                db.session.add(new_course)
        
        db.session.commit()
        return "Courses added successfully!"
    except Exception as e:
        db.session.rollback()
        return f"Error adding courses: {str(e)}"

@main_bp.route('/enroll/<int:course_id>', methods=['POST'])
def enroll_course(course_id):
    if 'email' not in session:
        return jsonify({'error': 'Please login to enroll in courses'}), 401
    
    try:
        student = Student.query.filter_by(email=session['email']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        existing_enrollment = Enrollment.query.filter_by(
            student_id=student.id,
            course_id=course_id
        ).first()
        
        if existing_enrollment:
            return jsonify({'message': 'You are already enrolled in this course', 'course_url': url_for('main.app_academy_course_details', course_id=course_id)})
        
        new_enrollment = Enrollment(
            student_id=student.id,
            course_id=course_id
        )
        db.session.add(new_enrollment)
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully enrolled in the course!',
            'course_url': url_for('main.app_academy_course_details', course_id=course_id)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@main_bp.route("/logout", methods=["GET", "POST"])  
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('main.app_academy_dashboard'))

@main_bp.route('/app_academy_course_details/<int:course_id>', endpoint='app_academy_course_details')
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('app_academy_course_details.html', course=course)

@main_bp.route('/app_academy_course')
def app_academy_course():
    return render_template("app_academy_course.html")

@main_bp.route('/api/courses')
def api_courses():
    page = request.args.get('page', 1, type=int)
    filter_value = request.args.get('filter', 'all courses')
    search_query = request.args.get('search', '').strip()
    
    query = Course.query
    
    if search_query:
        query = query.filter(
            db.or_(
                Course.title.ilike(f'%{search_query}%'),
                Course.description.ilike(f'%{search_query}%')
            )
        )
    
    if filter_value != 'all courses':
        query = query.filter(Course.title.ilike(f'%{filter_value}%'))
    
    per_page = 6
    paginated_courses = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'courses': [{
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'image_url': 'https://demos.themeselection.com/materio-bootstrap-html-admin-template/assets/img/pages/app-academy-tutor-1.png'
        } for course in paginated_courses.items],
        'total': paginated_courses.total,
        'pages': paginated_courses.pages,
        'current_page': page
    })