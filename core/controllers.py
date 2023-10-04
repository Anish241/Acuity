from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Course, Budget, Expense, Notes, DOCS, TodoList, Assignment
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def login_controller(username,password):
    user = authenticate(username=username, password=password)
    return user

    
    
        
def signupController(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("emailaddress")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username Taken")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email Taken")
            return redirect("register")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            fname = request.POST.get("firstname")
            lname = request.POST.get("lastname")
            college = request.POST.get("college")
            branch = request.POST.get("branch")
            year = request.POST.get("year")
            age = request.POST.get("age")
            if request.FILES.get("image") == None:
                profile = Profile.objects.create(user=user, first_name=fname, last_name=lname, college=college, branch=branch, year=year, email=email, age=age)
                profile.save()
            else:
                image = request.FILES.get("image")
                profile = Profile.objects.create(user=user, first_name=fname, last_name=lname, college=college, branch=branch, year=year, profileimg=image, email=email, age=age)
                profile.save()
        return True
    return False
    
def logoutController(request):
    auth.logout(request)
    return True

def getProfileController(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return profile

def attendence_manager_controller(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    course_obj = Course.objects.filter(user=user)

    if request.method=='POST':
        course_id = request.POST.get("course_id")
        course_obj = Course.objects.get(id=course_id)
        course_obj.lec_missed = course_obj.lec_missed + 1
        course_obj.lec_can_be_missed = course_obj.total_lecs -  course_obj.lec_missed - int(course_obj.total_lecs * course_obj.minimum_attendance / 100)
        course_obj.save()
    return course_obj

def course_form_controller(request,user):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        total_lecs = request.POST.get("total_lecs")
        minimum_attendance = request.POST.get("min_attendance")
        course = Course.objects.create(user=user, course_name=course_name, total_lecs=total_lecs, minimum_attendance=minimum_attendance)
        course.save()
        return True
    return False

def budgetManagerController(user):
    profile_obj = Profile.objects.get(user=user)
    expense_obj = Expense.objects.filter(user=user)
    budget_obj = Budget.objects.filter(user=user)   
    return profile_obj,expense_obj,budget_obj

def budgetFormController(request,user):
    if request.method == "POST":
        expense_name = request.POST.get("expense_name")
        expense_limit = request.POST.get("expense_limit")
        expense = Expense.objects.create(user=user, expense_name=expense_name, expense_limit=expense_limit)
        expense.save()
        return True
    return False

def deletecController(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)
        course.delete()
        return True
    return False

def bformController(request):
    if request.method == "POST":
        if Budget.objects.filter(user=request.user).exists():
            budget_obj = Budget.objects.get(user=request.user)
            budget_obj.delete()
        user= request.user
        month = request.POST.get("month")
        total_budget = request.POST.get("total_budget")
        budget = Budget.objects.create(user=user, month=month, budget_amount=total_budget)
        budget.save()
        return True
    return False

def addbController(request):
    if request.method == "POST":
        user = request.user
        budget_obj = Budget.objects.get(user=user)
        id = request.POST.get("expense_id")
        expense_obj = Expense.objects.get(id=id)
        expense_obj.expense_amount = int(expense_obj.expense_amount) + int(request.POST.get("expense_amount"))
        expense_obj.amount_remaining = int(expense_obj.expense_limit) - int(expense_obj.expense_amount)
        expense_obj.save()
        budget_obj.budget_amount = int(budget_obj.budget_amount) - int(request.POST.get("expense_amount"))
        budget_obj.save()
        return True
    return False

def deletebController(request):
    if request.method == "POST":
        user = request.user
        expense_obj = Expense.objects.get(id=request.POST.get("expense_id"))
        expense_obj.delete()
        return True
    return False

def noteformController(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        notes = Notes.objects.create(user=user, title=title, description=description)
        notes.save()
        return True
    return False

def deletenController(request):
    if request.method == "POST":
        notes_obj = Notes.objects.get(id=request.POST.get("note_id"))
        notes_obj.delete()
        return True
    return False

def todolistController(request):
    user = request.user
    todo_obj = TodoList.objects.filter(user=user)
    return todo_obj

def todoFormController(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        todo = TodoList.objects.create(user=user, title=title, description=description, due_date=due_date)
        todo.save()
        return True
    return False

def markController(request):
    if request.method == "POST":
        todo_obj = TodoList.objects.get(id=request.POST.get("todo_id"))
        if todo_obj.status == True:
            todo_obj.status = False
        else:
             todo_obj.status = True
        todo_obj.save()
        return True
    return False

def deletetController(request):
    if request.method == "POST":
        todo_obj = TodoList.objects.get(id=request.POST.get("todo_id"))
        todo_obj.delete()
        return True
    return False

def assignmentController(request):
    user = request.user
    assignment_obj = Assignment.objects.filter(user=user)
    return assignment_obj

def assignmentformController(request):
    if request.method == "POST":
        user = request.user
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assignment = Assignment.objects.create(user=user, subject=subject, description=description, due_date=due_date)
        assignment.save()
        return True
    return False

def deleteaController(request):
    if request.method == "POST":
        assignment_obj = Assignment.objects.get(id=request.POST.get("assignment_id"))
        assignment_obj.delete()
        return True
    return False
