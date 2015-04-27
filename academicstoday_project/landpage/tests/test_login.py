import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import login
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class LoginTest(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()
    
    def setUp(self):
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        student = Student.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

    def test_root_url_resolves_to_login_modal_view(self):
        found = resolve('/login_modal')
        self.assertEqual(found.func,login.login_modal)

    def test_login_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/login_modal')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'login_modal',response.content)
        self.assertIn(b'loginForm',response.content)
