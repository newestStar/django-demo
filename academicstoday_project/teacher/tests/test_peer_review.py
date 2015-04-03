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
from registrar.models import Teacher
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
from registrar.models import PeerReview


# View
from teacher.views import peer_review

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Create your tests here.
class PeerReviewTestCase(TestCase):
    def tearDown(self):
        User.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Assignment.objects.all().delete()
        AssignmentSubmission.objects.all().delete()
        EssayQuestion.objects.all().delete()
        ResponseQuestion.objects.all().delete()
        EssaySubmission.objects.all().delete()
        ResponseSubmission.objects.all().delete()
        PeerReview.objects.all().delete()

    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        ).save()
        user = User.objects.get(email=TEST_USER_EMAIL)
        student = Student.objects.create(user=user)
        teacher = Teacher.objects.create(user=user)
                                 
        # Create a test course.
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
                
        # Create our assignment
        assignment = Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )
        EssayQuestion.objects.create(
            question_id=1,
            assignment=assignment,
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        e_question = EssayQuestion.objects.get(question_id=1)
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=assignment,
            title="Hideauze",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        r_question = ResponseQuestion.objects.get(question_id=4)
    
        # Create our submission
        AssignmentSubmission.objects.create(
            submission_id=1,
            student=student,
            assignment=assignment,
        )
        submission = AssignmentSubmission.objects.get(assignment_id=1)
        EssaySubmission.objects.create(
            submission_id=1,
            student=student,
            question=e_question,
        )
        ResponseSubmission.objects.create(
            submission_id=2,
            student=student,
            question=r_question,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client
    
    def test_url_resolves_to_peer_review_page_view(self):
        found = resolve('/teacher/course/1/peer_reviews')
        self.assertEqual(found.func, peer_review.peer_reviews_page)

    def test_peer_reviews_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/peer_reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Peer Review',response.content)
        self.assertIn(b'view_submission(1);',response.content)

    def test_url_resolves_to_assignment_page_view(self):
        found = resolve('/teacher/course/1/peer_review/1')
        self.assertEqual(found.func, peer_review.assignment_page)
    
#    def test_assignment_page(self):
#        client = self.get_logged_in_client()
#        response = client.post('/teacher/course/1/peer_review/1')
#        self.assertEqual(response.status_code, 200)
#        self.assertIn(b'Comics Book Course',response.content)
#        self.assertIn(b'Peer Review',response.content)
#        self.assertIn(b'Assignment #1',response.content)

    def test_peer_review_modal_on_essay_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/teacher/course/1/peer_review/1/peer_review_modal',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'submission_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'peer_review_modal',response.content)

    def test_peer_review_modal_on_response_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/teacher/course/1/peer_review/1/peer_review_modal',{
            'question_id': 1,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'submission_id': 4,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'peer_review_modal',response.content)

    def test_save_peer_review_on_essay_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'submission_id': 1,
            'marks': 5,
        },**kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

    def test_save_peer_review_on_response_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'submission_id': 2,
            'marks': 5,
        },**kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

    def test_delete_peer_review_on_empty(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/teacher/course/1/peer_review/1/delete_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'review_id': 1,
        },**kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record does not exist')

    def test_delete_peer_review_on_essay_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'submission_id': 1,
            'marks': 5,
        },**kwargs)
        response = client.post('/course/1/peer_review/1/delete_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'review_id': 1,
        },**kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')

    def test_delete_peer_review_on_response_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'submission_id': 2,
            'marks': 5,
        },**kwargs)
        response = client.post('/teacher/course/1/peer_review/1/delete_peer_review',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'review_id': 2,
        },**kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

    def test_update_peer_review_on_essay_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'submission_id': 1,
            'marks': 5,
        },**kwargs)
        response = client.post('/teacher/course/1/peer_review/1/update_assignment_marks',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'review_id': 1,
            'marks': 3,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'updated')

    def test_update_peer_review_on_response_question(self):
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client.post('/teacher/course/1/peer_review/1/save_peer_review',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'submission_id': 2,
            'marks': 5,
        },**kwargs)
        response = client.post('/teacher/course/1/peer_review/1/update_assignment_marks',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'review_id': 2,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'updated')
        self.assertEqual(array['status'], 'success')

