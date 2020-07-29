from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

admin.site.register(Question)
# admin.site.register(Choice)
# admin.site.register(User)
# admin.site.register(FinalChoice)
# admin.site.register(FlashChoice)
# Register your models here.
@admin.register(Choice)
class ChoiceAdmin(ImportExportModelAdmin):
	pass
	# exclude = ('question', 'flash', 'ambient', 'flashTemp')

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
	pass	
admin.site.register(Questuser)	