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
from registrar.models import Student
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission


# View
from student.views import assignment

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class AssignmentTestCase(TestCase):
    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        ).save()
        user = User.objects.get(email=TEST_USER_EMAIL)
        Student.objects.create(user=user).save()
        
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
        ).save()
        
        course = Course.objects.get(id=1)
        if course is None:
            self.assertTrue(False)

        # Create our assignment(s)
        Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        ).save()
        
        assignment = Assignment.objects.get(assignment_id=1)
        if assignment is None:
            self.assertTrue(False)

        # Create questions
        EssayQuestion.objects.create(
            question_id=1,
            assignment=assignment,
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            assignment=assignment,
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
            d="Transhumanists",
            d_is_correct=True,
            e="Heavenly Creatures",
            e_is_correct=True,
        )
        TrueFalseQuestion.objects.create(
            question_id=3,
            assignment=assignment,
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=assignment,
            title="Hideauze",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_assignments_page_view(self):
        found = resolve('/course/1/assignments')
        self.assertEqual(found.func, assignment.assignments_page)

    def test_assignments_page_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignments')

        # Verify we are in the correct course.
        self.assertIn(b'Comics Book Course',response.content)
        
        # Verify our assignment was listed.
        self.assertIn(b'view_assignment(1);',response.content)

    def test_url_resolves_to_assignment_table_view(self):
        found = resolve('/course/1/assignments_table')
        self.assertEqual(found.func, assignment.assignments_table)

    def test_assignments_table_returns_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignments_table')
        
        # Verify our assignment was listed.
        self.assertIn(b'view_assignment(1);',response.content)
    
    def test_url_resolves_to_delete_assignment(self):
        found = resolve('/course/1/delete_assignment')
        self.assertEqual(found.func, assignment.delete_assignment)
    
    def test_delete_assignment_with_no_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/delete_assignment',{
            'assignment_id': 1,
        }, **kwargs)
        
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'assignment was deleted')

    def test_url_resolves_to_assignment_page_view(self):
        found = resolve('/course/1/assignment/1')
        self.assertEqual(found.func, assignment.assignment_page)

    def test_assignment_page(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignment/1')
        
        # Verify our assignment was listed.
        self.assertIn(b'Assignment #1',response.content)

    def test_submit_e_assignment_answer_with_empty_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignment/1/submit_e_assignment_answer',{
            'question_id': 1,
        }, **kwargs)
    
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'missing file')

    def test_submit_e_assignment_answer_with_pdf_file_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/course/1/assignment/1/submit_e_assignment_answer',{
                'question_id': 1,
                'file': fp
            }, **kwargs)
            
        # Verify Response
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

        # Verify Database
        submission = EssaySubmission.objects.get(submission_id=1)
        self.assertTrue(submission is not None)

        # Finish up
        submission.delete()

    def test_submit_mc_assignment_answer_with_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignment/1/submit_mc_assignment_answer',{
            'question_id': 2,
            'answer': 'A',
        }, **kwargs)
            
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

    def test_submit_tf_assignment_answer_with_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignment/1/submit_tf_assignment_answer',{
            'question_id': 3,
            'answer': 'true',
        }, **kwargs)
            
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')
    

    def test_submit_r_assignment_answer_with_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignment/1/submit_r_assignment_answer',{
            'question_id': 4,
            'answer': 'Because of Global Cooling caused by abnormal solar hibernation.',
        }, **kwargs)
            
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

# TODO:
# submit_assignment(request, course_id, assignment_id):
# compute_score(student, assignment, submission):

