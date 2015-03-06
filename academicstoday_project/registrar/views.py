from django.shortcuts import render
from django.core import serializers
from course.models import Student
from course.models import Teacher
from landpage.models import CoursePreview
from course.models import Course
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from registrar.forms import CourseForm

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/
#
# (3) Custom Forms Templates
# https://docs.djangoproject.com/en/1.7/topics/forms/#working-with-form-templates
#
# (4) DB Model Queries
# https://docs.djangoproject.com/en/1.7/topics/db/queries/

@login_required(login_url='/landpage')
def courses_page(request):
    courses = Course.objects.all()

    # Create our student account which will build our registration around.
    try:
         student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
         student = Student.objects.create(user=request.user)

    return render(request, 'registrar/courses/list.html',{
        'courses' : courses,
        'student' : student,
        'user' : request.user,
        'tab' : 'courses',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required()
def enrol(request):
    response_data = {'status' : 'failure', 'message' : 'unsupported request format'}
    if request.is_ajax():
        course_id = int(request.POST['course_id'])
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=course_id)

        # Lookup the course in the students enrolment history and if the
        # student is not enrolled, then enrol them now.
        try:
            found_course = Student.objects.get(courses__id=course_id)
        except Student.DoesNotExist:
            student.courses.add(course)
        response_data = {'status' : 'success', 'message' : 'enrolled' }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def my_courses_page(request):
    # Create our teacher account which will build our registration around.
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = Teacher.objects.create(user=request.user)

    return render(request, 'registrar/my_courses/list.html',{
        'teacher' : teacher,
        'user' : request.user,
        'tab' : 'my_courses',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required(login_url='/landpage')
def new_course_modal(request):
    if request.method == u'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
    else:
        course_form = CourseForm()

    return render(request, 'registrar/my_courses/new_course_modal.html',{
        'course_form' : course_form,
    })


@login_required(login_url='/landpage')
def save_new_course(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                teacher = Teacher.objects.get(user=request.user)
                teacher.courses.add(form.instance)
                response_data = {'status' : 'success', 'message' : 'unknown error with saving'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def course_delete(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                course_id = int(request.POST['course_id'])
                teacher = Teacher.objects.get(user=request.user)
                course = Course.objects.get(id=course_id)
                course.delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except Teacher.DoesNotExist:
                response_data = {'status' : 'failure', 'message' : 'no teacher'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
