from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from student.views import announcement
from student.views import syllabus
from student.views import policy
from student.views import lecture
from student.views import assignment
from student.views import quiz
from student.views import exam
from student.views import discussion
from student.views import peer_review

urlpatterns = patterns('',
    # Announcement
    url(r'^course/(\d+)/$', announcement.announcements_page),
    url(r'^course/(\d+)/home$', announcement.announcements_page),
    url(r'^course/(\d+)/announcement$', announcement.announcements_page),

    # Syllabus
    url(r'^course/(\d+)/syllabus$', syllabus.syllabus_page),

    # Grades & Policy
    url(r'^course/(\d+)/policy$', policy.policy_page),

    # Lecture
    url(r'^course/(\d+)/lectures$', lecture.lectures_page),
    url(r'^course/(\d+)/lecture$', lecture.lecture),

    # Assignment(s)
    url(r'^course/(\d+)/assignments$', assignment.assignments_page),
    url(r'^course/(\d+)/delete_assignment$', assignment.delete_assignment),
                       
    # Assignment
    url(r'^course/(\d+)/assignment/(\d+)$', assignment.assignment_page),
    url(r'^course/(\d+)/assignment/(\d+)/submit_assignment$', assignment.submit_assignment),
    url(r'^course/(\d+)/assignment/(\d+)/submit_e_assignment_answer$', assignment.submit_e_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_mc_assignment_answer$', assignment.submit_mc_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_tf_assignment_answer$', assignment.submit_tf_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_r_assignment_answer$', assignment.submit_r_assignment_answer),
                       
    # Quiz(zes)
    url(r'^course/(\d+)/quizzes$', quiz.quizzes_page),
    url(r'^course/(\d+)/quiz_delete$', quiz.delete_quiz),
                       
    # Quiz
    url(r'^course/(\d+)/quiz/(\d+)$', quiz.quiz_page),
    url(r'^course/(\d+)/quiz/(\d+)/submit_quiz$', quiz.submit_quiz),
    url(r'^course/(\d+)/quiz/(\d+)/submit_tf_quiz_answer$', quiz.submit_tf_assignment_answer),

    # Exam(s)
    url(r'^course/(\d+)/exams$', exam.exams_page),
    url(r'^course/(\d+)/delete_exam$', exam.delete_exam),
                       
    # Exam
    url(r'^course/(\d+)/exam/(\d+)$', exam.exam_page),
    url(r'^course/(\d+)/exam/(\d+)/submit_exam$', exam.submit_exam),
    url(r'^course/(\d+)/exam/(\d+)/submit_mc_exam_answer$', exam.submit_mc_exam_answer),

    # Peer-Review
    url(r'^course/(\d+)/peer_review$', peer_review.peer_review_page),
    url(r'^course/(\d+)/peer_review/(\d+)$', peer_review.assignment_page),

    # Discussion
    url(r'^course/(\d+)/discussion$', discussion.discussion_page),
)
