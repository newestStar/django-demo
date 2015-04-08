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
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Quiz
from registrar.models import QuizSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission
from student.views import quiz


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class QuizTestCase(TestCase):
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()
        for id in range(1, 10):
            try:
                Course.objects.get(id=id).delete()
            except Course.DoesNotExist:
                pass

    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        Student.objects.create(user=user).save()
        
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        ).save()
        
        course = Course.objects.get(id=1)
        if course is None:
            self.assertTrue(False)

        # Create our quiz
        Quiz.objects.create(
            quiz_id=1,
            quiz_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )
        quiz = Quiz.objects.get(quiz_id=1)
        
        # Create questions
        TrueFalseQuestion.objects.create(
            question_id=1,
            quiz=quiz,
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_quizzes_page_view(self):
        found = resolve('/course/1/quizzes')
        self.assertEqual(found.func, quiz.quizzes_page)

    def test_quizzes_page_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/quizzes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'view_quiz(1);',response.content)

    def test_url_resolves_to_quizzes_table_view(self):
        found = resolve('/course/1/quizzes_table')
        self.assertEqual(found.func, quiz.quizzes_table)

    def test_quizzes_table_returns_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/quizzes_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'view_quiz(1);',response.content)

    def test_url_resolves_to_delete_quiz(self):
        found = resolve('/course/1/quiz_delete')
        self.assertEqual(found.func, quiz.delete_quiz)

    def test_delete_quiz_with_no_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/quiz_delete',{
            'quiz_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'quiz was deleted')

    def test_url_resolves_to_quiz_page_view(self):
        found = resolve('/course/1/quiz/1')
        self.assertEqual(found.func, quiz.quiz_page)

    def test_quiz_page(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/quiz/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quiz #1',response.content)
    
    def test_submit_tf_assignment_answer_with_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/quiz/1/submit_tf_quiz_answer',{
            'question_id': 1,
            'answer': 'true',
        }, **kwargs)
        
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')

    def test_submit_quiz_without_answering_questions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/quiz/1/submit_quiz',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')

    def test_submit_quiz_with_answering_questions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        client.post('/course/1/quiz/1/submit_tf_quiz_answer',{
            'question_id': 1,
            'answer': 'true',
        }, **kwargs)
        response = client.post('/course/1/quiz/1/submit_quiz',{}, **kwargs)
        
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')