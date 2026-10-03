from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'


def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        # Create or get enrollment for current user
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> Create a submit view to handle exam submission
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    # Get user enrollment
    try:
        enrollment = Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        enrollment = Enrollment.objects.create(user=user, course=course)

    # Extract selected choices from POST request
    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choice_ids.append(int(value))
    
    if 'choice' in request.POST:
        selected_choice_ids.extend([int(x) for x in request.POST.getlist('choice')])

    selected_choice_ids = list(set(selected_choice_ids))

    # Create submission object and assign selected choices
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(selected_choice_ids)
    submission.save()

    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


# <HINT> Create a show_exam_result view to evaluate and display exam score
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = list(submission.choices.values_list('id', flat=True))

    total_score = 0
    total_grade = 0

    # Calculate total grade and earned score
    for question in Question.objects.filter(lesson__course=course):
        total_grade += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    score = round((total_score / total_grade) * 100) if total_grade > 0 else 0

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'submission': submission,
        'score': score,
        'total_score': total_score,
        'total_grade': total_grade
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
