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
#    url(r'^course/(\d+)/assignment_delete$', assignment.assignment_delete),
#    url(r'^course/(\d+)/upload_essay_assignment$', assignment.upload_essay_assignment),
#    url(r'^course/(\d+)/submit_truefalse_assignment_answer$', assignment.submit_truefalse_assignment_answer),
#    url(r'^course/(\d+)/submit_response_assignment_answer$', assignment.submit_response_assignment_answer),
#    url(r'^course/(\d+)/submit_mc_assignment_completion$', assignment.submit_mc_assignment_completion),
#    url(r'^course/(\d+)/submit_truefalse_assignment_completion$', assignment.submit_truefalse_assignment_completion),
#    url(r'^course/(\d+)/submit_response_assignment_completion$', assignment.submit_response_assignment_completion),

    # Assignment
    url(r'^course/(\d+)/assignment/(\d+)$', assignment.assignment_page),
    url(r'^course/(\d+)/assignment/(\d+)/submit_mc_assignment_answer$', assignment.submit_mc_assignment_answer),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_type_modal$', assignment.question_type_modal),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_essay_modal$', assignment.question_essay_modal),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_multiple_choice_modal$', assignment.question_multiple_choice_modal),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_true_false_modal$', assignment.question_true_false_modal),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_response_modal$', assignment.question_response_modal),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/save_question$', assignment.save_question),
#    url(r'^teacher/course/(\d+)/assignment/(\d+)/delete_question$', assignment.delete_question),
                       
    # Quiz
    url(r'^course/(\d+)/quizzes$', quiz.quizzes_page),
    url(r'^course/(\d+)/quiz_truefalse$', quiz.quiz_truefalse),
    url(r'^course/(\d+)/submit_truefalse_quiz_answer$', quiz.submit_truefalse_quiz_answer),
    url(r'^course/(\d+)/submit_truefalse_quiz_completion$', quiz.submit_truefalse_quiz_completion),
    url(r'^course/(\d+)/quiz_delete$', quiz.quiz_delete),

    # Exam
    url(r'^course/(\d+)/exams$', exam.exams_page),
    url(r'^course/(\d+)/exam_multiplechoice$', exam.exam_multiplechoice),
    url(r'^course/(\d+)/submit_mc_exam_answer$', exam.submit_mc_exam_answer),
    url(r'^course/(\d+)/submit_mc_exam_completion$', exam.submit_mc_exam_completion),
    url(r'^course/(\d+)/exam_delete$', exam.exam_delete),

    # Peer-Review
    url(r'^course/(\d+)/peer_review$', peer_review.peer_review_page),

    # Discussion
    url(r'^course/(\d+)/discussion$', discussion.discussion_page),
)
