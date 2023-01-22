from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("attendance_manager/", views.attedance_manager, name="attendance_manager"),
    path("courseform/", views.courseform, name="courseform"),
    path("budget_manager/", views.budget_manager, name="budget_magager"),
    path("budgetform/", views.budgetform, name="budgetform"),
    path("bform/", views.bform, name="bform"),
    path("attendance_manager/deletec/", views.deletec, name="deletec"),
    path("budget_manager/addb/", views.addb, name="addb"),
    path("budget_manager/deleteb/", views.deleteb, name="deleteb"), 
    path("notes/", views.notes, name="notes"),
    path("noteform/", views.noteform, name="noteform"), 
    path("notes/deleten/", views.deleten, name="deleten"),
    path("notes/deletef/", views.deletef, name="deletef"),
    path("todolist/", views.todolist, name="todolist"),
    path("todoform/", views.todoform, name="todoform"),
    path("todolist/mark/", views.mark, name="mark"),
    path("todolist/deletet/", views.deletet, name="deletet"),
    path("assignment/", views.assignment, name="assignment"),
    path("assignmentform/", views.assignmentform, name="assignmentform"),
    path("assignment/complete/", views.complete, name="complete"),
    path("assignment/deletea/", views.deletea, name="deletea"),
    path("settings/", views.settings, name="settings"),
    # pass the id in the url
    
    

]