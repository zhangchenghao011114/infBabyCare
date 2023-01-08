from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import HeadNurseInfo, Head2Nurse
from backlogic.models import NurseToPaientInfo
from django.utils.html import format_html
 
 
class HeadNurseInfoAdmin(admin.ModelAdmin):
    # Custom admin list view
    list_display = ('name', 'username', 'password', 'workPermitNumber', 'workPermitPassword', 'login_jwt',) 

    '''define which fields are editable on list view'''
    list_editable = ('username', )
    '''10 items per page'''
    list_per_page = 5
    '''Max 200 when clicking show all'''
    list_max_show_all = 200 #default
    # '''Calling select related objects to reduce SQL queries'''
    # list_select_related = ('username', )
    # '''Render a search box at top. ^, =, @, None=icontains'''
    # search_fields = ['username']
    '''Replacement value for empty field'''
    empty_value_display = 'NA'
    '''filter options'''
    list_filter = ('username', 'workPermitNumber', ) 
 
class Head2NurseAdmin(admin.ModelAdmin):
    list_display = ('headNurseWorkPermitNumber', 'nurseWorkPermitNumber',) 

    '''define which fields are editable on list view'''
    list_editable = ('nurseWorkPermitNumber', )
    '''10 items per page'''
    list_per_page = 5
    '''Max 200 when clicking show all'''
    list_max_show_all = 200 #default
    # '''Calling select related objects to reduce SQL queries'''
    # list_select_related = ('username', )
    # '''Render a search box at top. ^, =, @, None=icontains'''
    # search_fields = ['username']
    '''Replacement value for empty field'''
    empty_value_display = 'NA'
    '''filter options'''
    list_filter = ('headNurseWorkPermitNumber', ) 

class Nurse2PatientAdmin(admin.ModelAdmin):
    list_display = ('InpatientNumber','nurseWorkPermitNumber', ) 

    '''define which fields are editable on list view'''
    list_editable = ('nurseWorkPermitNumber', )
    '''10 items per page'''
    list_per_page = 5
    '''Max 200 when clicking show all'''
    list_max_show_all = 200 #default
    '''Replacement value for empty field'''
    empty_value_display = 'NA'
    '''filter options'''
    list_filter = ('nurseWorkPermitNumber', ) 

admin.site.register(HeadNurseInfo,HeadNurseInfoAdmin)
admin.site.register(Head2Nurse,Head2NurseAdmin)
admin.site.register(NurseToPaientInfo,Nurse2PatientAdmin)