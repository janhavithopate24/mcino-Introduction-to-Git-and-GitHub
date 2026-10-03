import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Instructor, Learner, Enrollment

def populate():
    print("Populating database...")
    
    # Create superuser / admin if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
        admin_user.first_name = 'Admin'
        admin_user.save()
        print("Created superuser 'admin'")

    # Create learner / student if not exists
    student_user, created = User.objects.get_or_create(
        username='student1',
        defaults={'email': 'student1@example.com', 'first_name': 'Alice'}
    )
    if created:
        student_user.set_password('studentpass123')
        student_user.save()
        Learner.objects.create(user=student_user, occupation='student', social_link='https://example.com')
        print("Created student user 'student1'")

    # Create Instructor
    instructor_user, _ = User.objects.get_or_create(username='instructor1', defaults={'email': 'inst@example.com', 'first_name': 'Prof. Py'})
    instructor, _ = Instructor.objects.get_or_create(user=instructor_user, defaults={'total_learners': 100})

    # Create Course
    course, _ = Course.objects.get_or_create(
        name='Introduction to Python',
        defaults={
            'description': 'Learn Python fundamentals including syntax, data types, control structures, and OOP.',
            'pub_date': date.today()
        }
    )
    course.instructors.add(instructor)

    # Create Enrollment for student
    Enrollment.objects.get_or_create(user=student_user, course=course)

    # Create Lesson 1
    lesson1, _ = Lesson.objects.get_or_create(
        title='Python Basics',
        course=course,
        defaults={'order': 1, 'content': 'Python is a high-level, interpreted programming language.'}
    )

    # Question 1 & Choices
    q1, _ = Question.objects.get_or_create(
        lesson=lesson1,
        question_text='What is the output of print(2 * 3 + 1)?',
        defaults={'grade': 5}
    )
    Choice.objects.get_or_create(question=q1, choice_text='6', defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q1, choice_text='7', defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q1, choice_text='5', defaults={'is_correct': False})

    # Question 2 & Choices
    q2, _ = Question.objects.get_or_create(
        lesson=lesson1,
        question_text='How do you start an if statement in Python?',
        defaults={'grade': 5}
    )
    Choice.objects.get_or_create(question=q2, choice_text='if x > 5 then', defaults={'is_correct': False})
    Choice.objects.get_or_create(question=q2, choice_text='if x > 5:', defaults={'is_correct': True})
    Choice.objects.get_or_create(question=q2, choice_text='if (x > 5)', defaults={'is_correct': False})

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
