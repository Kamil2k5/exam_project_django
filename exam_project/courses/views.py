from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson, Review
from .forms import CourseForm, LessonForm, ReviewForm


def course_list(request):
    query = request.GET.get('q')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'courses/course_list.html', {
        'courses': courses
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    reviews = course.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'avg_rating': avg_rating
    })


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('course_list')

    return render(request, 'courses/course_confirm_delete.html', {
        'course': course
    })


@login_required
def lesson_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', pk=course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/lesson_form.html', {'form': form})


@login_required
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'courses/lesson_form.html', {'form': form})


@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_id = lesson.course.id

    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', pk=course_id)

    return render(request, 'courses/lesson_confirm_delete.html', {
        'lesson': lesson
    })


@login_required
def review_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_detail', pk=course.id)
    else:
        form = ReviewForm()

    return render(request, 'courses/review_form.html', {'form': form})