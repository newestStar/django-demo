from django.db import models

# Create your models here.

# Developers Note:
#     (1) Database
#     Once you make a change, go to /src/academicstoday_project and type:
#     $ python manage.py makemigrations webapp
#     $ python manage.py migrate webapp
#
#     (2) Field Types
#     https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types
#
#     (3) Meta Options
#     https://docs.djangoproject.com/en/1.7/ref/models/options/
#
#     (4) Query Sets
#     https://docs.djangoproject.com/en/1.7/ref/models/querysets/
#
#     (5) Models
#     https://docs.djangoproject.com/en/1.7/topics/db/models/
#
#     (6) Model Instances
#     https://docs.djangoproject.com/en/1.7/ref/models/instances/
#

class LandpageTeamMember(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    full_name = models.CharField(max_length=31)
    role = models.CharField(max_length=31)
    twitter_url = models.CharField(max_length=255)
    facebook_url = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    linkedin_url = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
                                            
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_landpage_team_members'


class LandpageCoursePreview(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_landpage_course_previews'


class CoursePreview(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=63)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    description = models.TextField()
    summary = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_course_previews'


class Course(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=63)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    paragraph_one = models.CharField(max_length=255)
    paragraph_two = models.CharField(max_length=255)
    paragraph_three = models.CharField(max_length=255)
    start_date = models.DateField()
    finish_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_courses'

class CourseEnrollment(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.IntegerField(max_length=11)
    user_id = models.IntegerField(max_length=11)
    
    @classmethod
    def create(cls, course_id, user_id):
        enrollment = cls(course_id=course_id, user_id=user_id)
        return enrollment
    
    def __str__(self):
        return self.course_id + ' ' + self.user_id
    
    class Meta:
        db_table = 'at_course_enrollments'