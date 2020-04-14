from django.contrib import admin

from .models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(User)
# admin.site.register(FinalChoice)
# admin.site.register(FlashChoice)
# Register your models here.
