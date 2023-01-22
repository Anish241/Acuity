from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import Course
from .models import Budget
from .models import Expense
from .models import Notes
from .models import DOCS
from .models import TodoList
from .models import Assignment


admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Notes)
admin.site.register(DOCS)
admin.site.register(TodoList)
admin.site.register(Assignment)

