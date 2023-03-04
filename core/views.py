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



# Create your views here.
@login_required(login_url='/login')
def home(request):
    user = request.user
    return render(request, "dashboard/home.html", {'user': user})
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username or Password is incorrect")
            return redirect("login")
    return render(request, "login/login.html", {})


def register(request):
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
        return redirect("login")
    return render(request, "register/register.html", {})

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect("/login")

@login_required(login_url='/login')
def profile(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    return render(request, "profile/profile.html", {'profile_obj': profile_obj})

@login_required(login_url='/login')
def attedance_manager(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    course_obj = Course.objects.filter(user=user)

    if request.method=='POST':
        course_id = request.POST.get("course_id")
        course_obj = Course.objects.get(id=course_id)
        course_obj.lec_missed = course_obj.lec_missed + 1
        course_obj.lec_can_be_missed = course_obj.total_lecs -  course_obj.lec_missed - int(course_obj.total_lecs * course_obj.minimum_attendance / 100)
        course_obj.save()
        return redirect("attendance_manager")

   
  
    
    return render(request, "attendance_manager/attendance_manager.html", { 'course_obj': course_obj})

@login_required(login_url='/login')
def courseform(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        total_lecs = request.POST.get("total_lecs")
        minimum_attendance = request.POST.get("min_attendance")
        course = Course.objects.create(user=user, course_name=course_name, total_lecs=total_lecs, minimum_attendance=minimum_attendance)
        course.save()
        return redirect("attendance_manager")
 
        
    return render(request, "attendance_manager/courseform.html", {'profile_obj': profile_obj})

@login_required(login_url='/login')
def budget_manager(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    expense_obj = Expense.objects.filter(user=user)
    budget_obj = Budget.objects.filter(user=user)   
    return render(request, "Budget_Manager/budget_manager.html", {'expense_obj': expense_obj, 'profile_obj': profile_obj,'budget_obj': budget_obj})

@login_required(login_url='/login')
def budgetform(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    if request.method == "POST":
        expense_name = request.POST.get("expense_name")
        expense_limit = request.POST.get("expense_limit")
        expense = Expense.objects.create(user=user, expense_name=expense_name, expense_limit=expense_limit)
        expense.save()
        return redirect("/budget_manager")
    return render(request, "Budget_Manager/budgetform.html", {})

@login_required(login_url='/login')
def deletec(request):
    user = request.user
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course_obj = Course.objects.get(id=course_id)
        course_obj.delete()
        return redirect("/attendance_manager")
    return render(request, "attendance_manager/deletec.html", {})

@login_required(login_url='/login')
def bform(request):
    if request.method == "POST":
        if Budget.objects.filter(user=request.user).exists():
            budget_obj = Budget.objects.get(user=request.user)
            budget_obj.delete()
        user= request.user
        month = request.POST.get("month")
        total_budget = request.POST.get("total_budget")
        budget = Budget.objects.create(user=user, month=month, budget_amount=total_budget)
        budget.save()
        return redirect("/budget_manager")
    return render(request, "Budget_Manager/bform.html", {})
@login_required(login_url='/login')
def addb(request):
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
        return redirect("/budget_manager")

@login_required(login_url='/login')
def deleteb(request):
    if request.method == "POST":
        user = request.user
        expense_obj = Expense.objects.get(id=request.POST.get("expense_id"))
        expense_obj.delete()
        return redirect("/budget_manager")

@login_required(login_url='/login')
def notes(request):
    user = request.user
    notes_obj = Notes.objects.filter(user=user)
    if request.method == "POST":
        if "viewf" in request.POST:
            note_id = request.POST.get("note_id")
            notes_obj = Notes.objects.get(id=note_id)
            fs = DOCS.objects.filter(note_id=note_id)
           
            return render(request, "notes/filelist.html", {'notes_obj': notes_obj,'fs': fs})
        elif "idbtn" in request.POST:
            notes_obj = Notes.objects.get(id=request.POST.get("note_id"))
            return render(request, "notes/fileform.html", {'notes_obj': notes_obj})
        else:
            name = request.POST.get("name")
            note_id = request.POST.get("note_id")
            notes_obj = Notes.objects.get(id=note_id)
            user = request.user
            file = request.FILES.get("file")
            if request.FILES.get("file") is not None:
                doc_obj = DOCS.objects.create(name=name, file=file, note_id=note_id, user=user)
                doc_obj.save()
                fs = DOCS.objects.filter(note_id=note_id)
                return render(request, "notes/filelist.html", {'notes_obj': notes_obj, 'fs': fs})
            else:
                doc_obj = DOCS.objects.create(name=name, note_id=note_id, user=user)
                doc_obj.save()
                fs = DOCS.objects.filter(note_id=note_id)
                return render(request, "notes/filelist.html", {'notes_obj': notes_obj, 'fs': fs})
       


    return render(request, "notes/notes.html", {'notes_obj': notes_obj})
    

@login_required(login_url='/login')
def noteform(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        notes = Notes.objects.create(user=user, title=title, description=description)
        notes.save()
       

        return redirect("/notes")
    
    return render(request, "notes/noteform.html")
@login_required(login_url='/login')
def deleten(request):
    if request.method == "POST":
        notes_obj = Notes.objects.get(id=request.POST.get("note_id"))
        notes_obj.delete()
        return redirect("/notes")

@login_required(login_url='/login')
def todolist(request):
    user = request.user
    todo_obj = TodoList.objects.filter(user=user)


    return render(request, "todolist/todolist.html", {'todo_obj': todo_obj})
@login_required(login_url='/login')
def deletef(request):
    if request.method == "POST":
        notes_obj = Notes.objects.get(id=request.POST.get("note_id"))
        fs = DOCS.objects.filter(note_id=request.POST.get("note_id"))
        doc_obj = DOCS.objects.get(id=request.POST.get("file_id"))
        doc_obj.delete()
        return render(request, "notes/filelist.html", {'notes_obj': notes_obj, 'fs': fs})
# store UUID later in this variable
@login_required(login_url='/login')
def todoform(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        todo = TodoList.objects.create(user=user, title=title, description=description, due_date=due_date)
        todo.save()
        return redirect("/todolist")
    return render(request, "todolist/todoform.html")
@login_required(login_url='/login')
def mark(request):
    if request.method == "POST":
        todo_obj = TodoList.objects.get(id=request.POST.get("todo_id"))
        if todo_obj.status == True:
            todo_obj.status = False
        else:
             todo_obj.status = True
        todo_obj.save()
        return redirect("/todolist") 

@login_required(login_url='/login')
def deletet(request):
    if request.method == "POST":
        todo_obj = TodoList.objects.get(id=request.POST.get("todo_id"))
        todo_obj.delete()
        return redirect("/todolist")

@login_required(login_url='/login')
def assignment(request):
    user = request.user
    assignment_obj = Assignment.objects.filter(user=user)
    return render(request, "assignment/assignment.html", {'assignment_obj': assignment_obj})

@login_required(login_url='/login')
def assignmentform(request):
    if request.method == "POST":
        user = request.user
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assignment = Assignment.objects.create(user=user, subject=subject, description=description, due_date=due_date)
        assignment.save()
        return redirect("/assignment")

    return render(request, "assignment/assignmentform.html")

@login_required(login_url='/login')
def complete(request):
    if request.method == "POST":
        assignment_obj = Assignment.objects.get(id=request.POST.get("assignment_id"))
        if assignment_obj.status == True:
            assignment_obj.status = False
        else:
             assignment_obj.status = True
        assignment_obj.save()
        return redirect("/assignment")
@login_required(login_url='/login')
def deletea(request):
    if request.method == "POST":
        assignment_obj = Assignment.objects.get(id=request.POST.get("assignment_id"))
        assignment_obj.delete()
        return redirect("/assignment")

@login_required(login_url='/login')
def settings(request):
    if request.method == "POST":
        if "imgbtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.profileimg = request.FILES.get("image")
            profile.save()
            return redirect("/settings")
        elif "passbtn" in request.POST:
                user = request.user
                if user.check_password(request.POST.get("oldpassword")):
                    user.set_password(request.POST.get("newpassword"))
                    user.save()
                else:
                    return HttpResponse("Old password is incorrect")
                return redirect("/settings")
        elif "fnamebtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.first_name = request.POST.get("fname")
            profile.save()
            return redirect("/settings")
        elif "lnamebtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.last_name = request.POST.get("lname")
            profile.save()
            return redirect("/settings")
        elif "emailbtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.email = request.POST.get("email")
            profile.save()
            return redirect("/settings")
        elif "collegebtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.college = request.POST.get("college")
            profile.save()
            return redirect("/settings")
        elif "branchbtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.branch = request.POST.get("branch")
            profile.save()
            return redirect("/settings")
        elif "yosbtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.year = request.POST.get("yos")
            profile.save()
            return redirect("/settings")
        elif "agebtn" in request.POST:
            user = request.user
            profile = Profile.objects.get(user=user)
            profile.age = request.POST.get("age")
            profile.save()
            return redirect("/settings")
        
    return render(request, "profile/settings.html")


