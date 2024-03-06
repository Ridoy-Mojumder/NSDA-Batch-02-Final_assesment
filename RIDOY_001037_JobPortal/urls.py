
from django.contrib import admin
from django.urls import path
from RIDOY_001037_JobPortal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('singupPage',singupPage,name="singupPage"),
    path('',singinPage,name="singinPage"),
    path('deshboardPage/',deshboardPage,name="deshboardPage"),
    path('logoutPage/',logoutPage,name="logoutPage"),
    path('addjobPage/',addjobPage,name="addjobPage"),
    path('deletePage/<str:myid>',deletePage,name="deletePage"),
    path('editPage/<str:myid>',editPage,name="editPage"),
    path('updatePage/',updatePage,name="updatePage"),
    path('applyPage/<str:myid>',applyPage,name="applyPage"),    
    path('viewjobPage',viewjobPage,name="viewjobPage"),    
    path('profilePage',profilePage,name="profilePage"), 
    path('EditprofilePage/',EditprofilePage,name="EditprofilePage"),
    path('changepassPage/',changepassPage,name="changepassPage"),
    path('createdjobbyrecruiter/',createdjobbyrecruiter,name="createdjobbyrecruiter"),
    path('createdresumebyjobseeker/',createdresumebyjobseeker,name="createdresumebyjobseeker"),
    path('viewresumepage/',viewresumepage,name="viewresumepage"),
    path('searchResultsPage/',searchResultsPage,name='searchResultsPage'),
    path('matching_profiles/<int:job_id>/', matching_profiles, name='matching_profiles'),
    path('skill-matching/', skill_matching_page, name='skillMatchingPage'),
    path('skill-matching/', skill_matching_page, name='skill_matching_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
