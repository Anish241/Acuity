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
from .controllers import *



# Create your views here.
@login_required(login_url='/login')
def home(request):
    user = request.user
    return render(request, "dashboard/home.html", {'user': user})
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = login_controller(username,password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username or Password is incorrect")
            return redirect("login")
    return render(request, "login/login.html", {})


def register(request):
        
    isReg = signupController(request)
    if isReg:
        return redirect("login")
    return render(request, "register/register.html", {})

@login_required(login_url='/login')
def logout(request):
    if logoutController(request):
        return redirect("/login")

@login_required(login_url='/login')
def profile(request):
    profile_obj = getProfileController(request)
    return render(request, "profile/profile.html", {'profile_obj': profile_obj})

@login_required(login_url='/login')
def attedance_manager(request):
       course_obj = attendence_manager_controller(request)
       return render(request, "attendance_manager/attendance_manager.html", { 'course_obj': course_obj})

@login_required(login_url='/login')
def courseform(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    if course_form_controller(request,user):
        return redirect("attendance_manager")
 
    return render(request, "attendance_manager/courseform.html", {'profile_obj': profile_obj})

@login_required(login_url='/login')
def budget_manager(request):
    user = request.user
    profile_obj, expense_obj, budget_obj = budgetManagerController(user)  
    return render(request, "Budget_Manager/budget_manager.html", {'expense_obj': expense_obj, 'profile_obj': profile_obj,'budget_obj': budget_obj})

@login_required(login_url='/login')
def budgetform(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    if budgetFormController(request,user):
        return redirect("/budget_manager")
    return render(request, "Budget_Manager/budgetform.html", {})

@login_required(login_url='/login')
def deletec(request):
    user = request.user
    if deletecController(request):
        return redirect("/attendance_manager")
    return render(request, "attendance_manager/deletec.html", {})

@login_required(login_url='/login')
def bform(request):
    if bformController(request):
        return redirect("/budget_manager")
    return render(request, "Budget_Manager/bform.html", {})
@login_required(login_url='/login')
def addb(request):
    if addbController(request):
        return redirect("/budget_manager")

@login_required(login_url='/login')
def deleteb(request):
    if deletebController(request):
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
    if noteformController(request):
       return redirect("/notes")
    
    return render(request, "notes/noteform.html")
@login_required(login_url='/login')
def deleten(request):
    if deleten(request):
        return redirect("/notes")

@login_required(login_url='/login')
def todolist(request):
    todo_obj = todolistController(request)


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
    if todoFormController(request):
        return redirect("/todolist")
    return render(request, "todolist/todoform.html")
@login_required(login_url='/login')
def mark(request):
    if markController(request):
        return redirect("/todolist") 

@login_required(login_url='/login')
def deletet(request):
    if deletecController(request):
        return redirect("/todolist")

@login_required(login_url='/login')
def assignment(request):
    assignment_obj = assignmentController(request)
    return render(request, "assignment/assignment.html", {'assignment_obj': assignment_obj})

@login_required(login_url='/login')
def assignmentform(request):
    if assignmentformController(request):
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
    if deleteaController(request):
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


