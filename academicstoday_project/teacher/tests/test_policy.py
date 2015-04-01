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
from registrar.models import Policy


# View
from teacher.views import policy

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Create your tests here.
class PolicyTestCase(TestCase):
    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        Teacher.objects.create(user=user)
                                 
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
        category="",
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_policy_page_view(self):
        found = resolve('/teacher/course/1/policy')
        self.assertEqual(found.func, policy.policy_page)
    
    def test_policy_page_without_pdf_file(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/policy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'<h1>Upload',response.content)

    def test_policy_modal(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/policy_modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'policy_modal',response.content)

    def test_policy_page_with_pdf_file(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_policy',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        response = client.post('/teacher/course/1/policy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_delete_policy',response.content)
        self.assertIn(b'PDF RESULT',response.content)

        try:
            Policy.objects.get(policy_id=1).delete()
        except Policy.DoesNotExist:
            pass
        try:
             Policy.objects.get(policy_id=2).delete()
        except Policy.DoesNotExist:
            pass
        try:
             Policy.objects.get(policy_id=3).delete()
        except Policy.DoesNotExist:
            pass

    def test_save_policy(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_policy',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
            json_string = response.content.decode(encoding='UTF-8')
            array = json.loads(json_string)
            self.assertEqual(array['message'], 'saved')
            self.assertEqual(array['status'], 'success')
        
        try:
            Policy.objects.get(policy_id=1).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=2).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=3).delete()
        except Policy.DoesNotExist:
            pass

    def test_delete_policy(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/save_policy',{
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        
        response = client.post('/teacher/course/1/delete_policy',{
            'policy_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')
        
        try:
            Policy.objects.get(policy_id=1).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=2).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=3).delete()
        except Policy.DoesNotExist:
            pass
