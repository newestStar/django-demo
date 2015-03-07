from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=127)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    is_official = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=settings.COURSE_UNAVAILABLE_STATUS)
    file = models.FileField(upload_to='uploads',null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_courses'


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'at_students'


class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'at_teachers'


class Announcement(models.Model):
    course = models.ForeignKey(Course)
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=31)
    body = models.TextField()
    post_date = models.DateField(auto_now=True, auto_now_add=True, null=True)

    @classmethod
    def create(cls, course_id, title, body, post_date):
        announcement = cls(course_id=course_id, title=title,
                           body=body, post_date=post_date)
        return announcement

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.body + ' ' + self.post_date;

    class Meta:
        db_table = 'at_announcements'

class Syllabus(models.Model):
    course = models.ForeignKey(Course)
    syllabus_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)

    def __str__(self):
        return self.file;

    class Meta:
        db_table = 'at_syllabus'

class Policy(models.Model):
    course = models.ForeignKey(Course)
    policy_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)

    def __str__(self):
        return self.policy_id + ' ' + self.file.url;

    class Meta:
        db_table = 'at_policys'

class Week(models.Model):
    week_id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    week_num = models.PositiveSmallIntegerField(max_length=7)
    title = models.CharField(max_length=31)
    description = models.TextField()

    def __str__(self):
        return self.course_id + ' ' + self.file_url;

    class Meta:
        db_table = 'at_weeks'

class Lecture(models.Model):
    course = models.ForeignKey(Course)
    lecture_id = models.AutoField(primary_key=True)
    lecture_num = models.PositiveSmallIntegerField(max_length=7, default=0)
    week_num = models.PositiveSmallIntegerField(max_length=7)
    title = models.CharField(max_length=31, default='',null=True)
    description = models.TextField(default='',null=True)
    youtube_url = models.URLField(default='',null=True)
    vimeo_url = models.URLField(default='',null=True)
    bliptv_url = models.URLField(default='',null=True)
    preferred_service = models.CharField(max_length=31)

    def __str__(self):
        return self.course_id + ' ' + self.file_url;

    class Meta:
        db_table = 'at_lectures'


class Exam(models.Model):
    course = models.ForeignKey(Course)
    exam_id = models.AutoField(primary_key=True)
    exam_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)

    def __str__(self):
        return self.course_id + ' ' + self.type;

    class Meta:
        db_table = 'at_exams'


class ExamSubmission(models.Model):
    course = models.ForeignKey(Course)
    exam = models.ForeignKey(Exam)
    student = models.ForeignKey(Student)
    submission_id = models.AutoField(primary_key=True)
    exam_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.submission_id + ' ' + self.type;

    class Meta:
        db_table = 'at_exam_submissions'


class Quiz(models.Model):
    course = models.ForeignKey(Course)
    quiz_id = models.AutoField(primary_key=True)
    quiz_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    due_date = models.DateField(null=True)

    def __str__(self):
        return self.quiz_id + ' ' + self.type;

    class Meta:
        db_table = 'at_quizzes'


class QuizSubmission(models.Model):
    course = models.ForeignKey(Course)
    submission_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student)
    quiz_id = models.PositiveIntegerField()
    quiz_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz_id + ' ' + self.type;

    class Meta:
        db_table = 'at_quiz_submissions'


class Assignment(models.Model):
    course = models.ForeignKey(Course)
    assignment_id = models.AutoField(primary_key=True)
    assignment_num = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=31, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)

    def __str__(self):
        return self.assignment_id + ' ' + self.type;

    class Meta:
        db_table = 'at_assignments'


class AssignmentSubmission(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(Student)
    submission_id = models.AutoField(primary_key=True)
    assignment_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.submission_id + ' ' + self.type;

    class Meta:
        db_table = 'at_assignment_submissions'


class EssayQuestion(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment)
    question_id = models.AutoField(max_length=11, primary_key=True)
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.question_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_essay_questions'

class EssaySubmission(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment)
    student = models.ForeignKey(Student)
    submission_id = models.AutoField(max_length=11, primary_key=True)
    file = models.FileField(upload_to='uploads')
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.course_id + ' ' + self.file_path;

    class Meta:
        db_table = 'at_essay_submissions'

class MultipleChoiceQuestion(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    exam = models.ForeignKey(Exam, null=True)
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    json_choices = models.CharField(max_length=1055, default='{}')
    json_answers = models.CharField(max_length=127, default='{}')

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_multiple_choice_questions'

class MultipleChoiceSubmission(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    student = models.ForeignKey(Student)
    exam = models.ForeignKey(Exam, null=True)
    submission_id = models.AutoField(max_length=11, primary_key=True)
    question_num = models.PositiveSmallIntegerField(default=0)
    json_answers = models.CharField(max_length=127, default='{}')
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)

    @classmethod
    def create(cls, assignment_id, exam_id, course_id, student_id, question_num):
        submission = cls(student_id=student_id,
                         course_id=course_id,
                         assignment_id=assignment_id,
                         exam_id=exam_id,
                         question_num=question_num)
        return submission

    def __str__(self):
        return self.course_id + ' ' + self.selected;

    class Meta:
        db_table = 'at_multiple_choice_submissions'


class TrueFalseQuestion(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    true_choice = models.CharField(max_length=127, null=True)
    false_choice = models.CharField(max_length=127, null=True)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_true_false_questions'


class TrueFalseSubmission(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    student = models.ForeignKey(Student)
    submission_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(default=0)
    answer = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.course_id + ' ' + self.selected;

    class Meta:
        db_table = 'at_true_false_submissions'


class ResponseQuestion(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    answer = models.TextField(default='')

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_response_questions'


class ResponseSubmission(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    student = models.ForeignKey(Student)
    submission_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(default=0)
    answer = models.TextField(default='')
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return self.course_id + ' ' + self.response;

    class Meta:
        db_table = 'at_response_submissions'


class AssignmentReview(models.Model):
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment, null=True)
    student = models.ForeignKey(Student)
    review_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=31)
    comment = models.TextField()
    marks = models.PositiveSmallIntegerField(default=0)
    post_date = models.DateField(auto_now=True, auto_now_add=True, null=True)

    @classmethod
    def create(cls, student_id, assignment_id, course_id, title, comment, marks):
        assignment = cls(
            student_id=student_id,
            assignment_id=assignment_id,
            course_id=course_id,
            title=title,
            comment=comment,
            marks=marks
        )
        return assignment

    def __str__(self):
        return self.id + ' ' + self.title + ' ' + self.comment + ' ' + self.post_date;

    class Meta:
        db_table = 'at_assignment_reviews'
