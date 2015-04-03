# Django & Python
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static, settings
import json

# Modal
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Syllabus


# View
from teacher.views import syllabus

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class SyllabusTestCase(TestCase):
    def tearDown(self):
        for id in range(1, 10):
            try:
                Syllabus.objects.get(syllabus_id=id).delete()
            except Syllabus.DoesNotExist:
                pass
    
    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
                                 
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_syllabus_page_view(self):
        found = resolve('/teacher/course/1/syllabus')
        self.assertEqual(found.func, syllabus.syllabus_page)
    
    def test_syllabus_page_without_pdf_file(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/syllabus')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'<h1>Upload Syllabus</h1>',response.content)

    def test_syllabus_modal(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/syllabus_modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'syllabus_modal',response.content)

    def test_syllabus_page_with_pdf_file(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_syllabus',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        response = client.post('/teacher/course/1/syllabus')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_delete_syllabus',response.content)
        self.assertIn(b'PDF RESULT',response.content)

    def test_save_syllabus(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_syllabus',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
            json_string = response.content.decode(encoding='UTF-8')
            array = json.loads(json_string)
            self.assertEqual(array['message'], 'saved')
            self.assertEqual(array['status'], 'success')

    def test_delete_syllabus(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_syllabus',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
            json_string = response.content.decode(encoding='UTF-8')
            array = json.loads(json_string)
            self.assertEqual(array['message'], 'saved')
            self.assertEqual(array['status'], 'success')
        
        response = client.post('/teacher/course/1/delete_syllabus',{
            'syllabus_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

