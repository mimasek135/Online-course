from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Choice, Enrollment, Submission

def index(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Validate IDs and reject choices belonging to another course.
    try:
        selected_ids = {int(value) for value in request.POST.getlist('choice')}
    except (ValueError, TypeError):
        return HttpResponseBadRequest('Invalid choice.')
    choices = list(Choice.objects.filter(pk__in=selected_ids, question__course=course))
    if len(choices) != len(selected_ids):
        return HttpResponseBadRequest('Invalid choice for this course.')
    with transaction.atomic():
        enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(choices)
    return redirect('onlinecourse:show_exam_result', course_id=course.pk, submission_id=submission.pk)

@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id,
        enrollment__course_id=course_id, enrollment__user=request.user)
    course = submission.enrollment.course
    selected_ids = set(submission.choices.values_list('pk', flat=True))
    total = earned = 0
    results = []
    for question in course.question_set.prefetch_related('choice_set').all():
        question_ids = {choice.pk for choice in question.choice_set.all()}
        correct = question.is_get_score(selected_ids & question_ids)
        total += question.grade
        earned += question.grade if correct else 0
        results.append({'question': question, 'correct': correct,
            'selected': [c for c in question.choice_set.all() if c.pk in selected_ids],
            'answers': [c for c in question.choice_set.all() if c.is_correct]})
    score = round(100 * earned / total, 2) if total else 0
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course, 'submission': submission, 'score': score,
        'earned': earned, 'total': total, 'passed': total > 0 and score >= 80, 'results': results})
