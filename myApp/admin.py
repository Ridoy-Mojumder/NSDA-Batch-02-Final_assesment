from django.contrib import admin
from myApp.models import *

class CUstom_User_Display(admin.ModelAdmin):
    list_display=['display_name','email','user_type']

    
admin.site.register(Custom_User,CUstom_User_Display)
admin.site.register(job_model)
admin.site.register(Recruiter_Profile)
admin.site.register(Jobseeker_Profile)
admin.site.register(jobapplyModel)