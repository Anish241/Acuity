from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    profileimg= models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100, default='course')
    total_lecs = models.IntegerField(default=0)
    lec_missed = models.IntegerField(default=0)
    minimum_attendance = models.IntegerField(default=0)
    lec_can_be_missed = models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=100, default='month')
    budget_amount = models.IntegerField(default=0)
    remaining_amount = models.IntegerField(default=0)

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=100, default='expense')
    expense_amount = models.IntegerField(default=0)
    expense_limit = models.IntegerField(default=0)
    amount_remaining = models.IntegerField(default=-1)

class Notes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='note')
    description = models.CharField(max_length=200, default='description')
    
class DOCS(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_id = models.CharField(max_length=100, default='note')
    #set the name of the file as the name of the uploaded file
    name = models.CharField(max_length=100, default='file')
    file = models.FileField(upload_to='docs', default='blank.pdf')
    
class TodoList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='title')
    description = models.CharField(max_length=200, default='description')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=False)

class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, default='subject')
    description = models.CharField(max_length=200, default='description')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=False)
