from django.contrib import admin

from .models import Question, Choice, FinalChoice

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(FinalChoice)

# Register your models here.
