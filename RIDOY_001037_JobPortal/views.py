from django.shortcuts import redirect,render
from django.http import HttpResponse
from myApp.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q

import random

def singupPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        displayName = request.POST.get('displayName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        userType = request.POST.get('userType')

        # Check if password and confirm password match
        if password != confirmPassword:
            return render(request, "signup.html", {'error': 'Passwords do not match'})

        user = Custom_User.objects.create_user(username=username, password=password)
        user.display_name = displayName
        user.email = email
        user.user_type = userType
        user.save()

        if user.user_type == "recruiter":
            recruiter_profile = Recruiter_Profile.objects.create(user=user)
            recruiter_profile.save()

        elif user.user_type == "jobseeker":
            jobseeker_profile = Jobseeker_Profile.objects.create(user=user)
            jobseeker_profile.save()

        return redirect("singinPage")

    return render(request, "signup.html")





def singinPage(request):

    if request.method =='POST':
        user_name=request.POST.get("username")
        password=request.POST.get("password")


        
        user=authenticate(request,username=user_name,password=password)
        
        if user:
            login(request,user)
            return redirect("deshboardPage")
    return render(request,"login.html")

@login_required
def deshboardPage(request):
    return render(request,"deshborad.html")




@login_required
def viewjobPage(request):
    job=job_model.objects.all()

    return render(request,'viewjob.html',{'job':job})

@login_required
def addjobPage(request):

    user=request.user


    if request.method == "POST":
        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')
        companydiscription=request.POST.get('companydescription')
        qualifications=request.POST.get('qualifications')
        deadline=request.POST.get('deadline')
        p_pic=request.FILES.get("profilePicture")

        job=job_model(
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            company_description=companydiscription,
            Qualifications=qualifications,
            deadline=deadline,
            Profile_Pic=p_pic,
            job_creator=user,
        )
        

        job.save()
        return redirect("viewjobPage")

    return render(request,"Recruiter/Addjob.html")
@login_required
def deletePage(request,myid):

    job=job_model.objects.filter(id=myid)
    job.delete()
    return redirect("viewjobPage")
@login_required
def editPage(request,myid):

    job=job_model.objects.filter(id=myid)

    return render(request,"Recruiter/editjob.html",{'job':job})

@login_required
def updatePage(request):
    
    user=request.user


    if request.method == "POST":
        jobid=request.POST.get('jobid')
        jobTitle=request.POST.get('jobTitle')
        companyName=request.POST.get('companyName')
        location=request.POST.get('location')
        description=request.POST.get('description')
        companydiscription=request.POST.get('companydescription')
        qualifications=request.POST.get('qualifications')
        deadline=request.POST.get('deadline')
        p_pic=request.FILES.get("profilePicture")

        job=job_model(
            id=jobid,
            job_title=jobTitle,
            company_name=companyName,
            location=location,
            description=description,
            company_description=companydiscription,
            Qualifications=qualifications,
            deadline=deadline,
            job_creator=user,
            Profile_Pic= p_pic,
        )
        job.save()
        return redirect("viewjobPage")
    

@login_required
def applyPage(request,myid):

    job=get_object_or_404(job_model,id=myid)

    if request.method == "POST":
        skills=request.POST.get("skills")
        resume=request.FILES.get("resume")

        if skills and resume:
            job_seeker=request.user
            applicant=jobapplyModel.objects.create(
            job=job,
            applicant=job_seeker,
            skills=skills,
            apply_resume=resume
            )

            applicant.save()
        
        else:
            messages.error(request,"Error in application")
        
        messages.success(request,"Apply successfully")
        return redirect("profilePage")
  

    return render(request,'JobSeeker/applyjob.html',{'job':job})

@login_required
def profilePage(request):

    return render(request,"profile.html")

@login_required
def EditprofilePage(request):

    user=request.user


    if request.method == "POST":

        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        displayName=request.POST.get('displayName')
        profilePicture=request.FILES.get('profilePicture')
        password=request.POST.get('password')
        resume=request.FILES.get('resumes')
        skills=request.POST.get('skills')

        if not check_password(password,user.password):
            messages.error(request,"Profile not update, wrong password")
            return redirect("EditprofilePage")
        
        user.firstName=firstName
        user.lastName=lastName
        user.display_name=displayName

        if user.user_type == "jobseeker":
            job_seeker_profile=user.jobseekerprofile
            job_seeker_profile.skils=skills
            job_seeker_profile.resumes=resume
            job_seeker_profile.save()


        if profilePicture:
            user.Profile_picture= profilePicture
        user.save()
        messages.success(request,"Profile update successfully")
        return redirect("profilePage")
    return render(request,"Editprofile.html",)




@login_required
def createdjobbyrecruiter(request):

    user= request.user

    creator=job_model.objects.filter(job_creator=user)


    return render(request,"createdjob.html",{'creator':creator})

@login_required
def createdresumebyjobseeker(request):

    user=request.user


    if request.method == "POST":

        resume=request.FILES.get('resumes')
        skills=request.POST.get('skills')




        if user.user_type == "jobseeker":
            job_seeker_profile=user.jobseekerprofile
            job_seeker_profile.skils=skills
            job_seeker_profile.resumes=resume
            job_seeker_profile.save()


        return redirect("profilePage")


    return render(request,"JobSeeker/createresume.html")



@login_required
def viewresumepage(request):

    return render(request,"viewresume.html")



def searchResultsPage(request):
    try:
        query = request.GET.get("search_query")

        if query:
            jobs = job_model.objects.filter(job_title__icontains=query)
            context = {
                'query': query,
                'jobs': jobs,
            }

            # Check if there are matching jobs
            if jobs:
                return render(request, 'search_results.html', context)
            else:
                return render(request, 'error.html', {'error_message': f'No matching jobs found for "{query}"'})
        else:
            return render(request, 'error.html', {'error_message': 'Invalid search query.'})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})



def matching_profiles(request, job_id):
    job = get_object_or_404(job, pk=job_id)
    job_skills = job.Qualifications.split(', ')

    matching_profiles = []

    # Get all job applicants
    job_applications = jobapplyModel.objects.filter(job=job)

    # Check each applicant's skills
    for application in job_applications:
        applicant_skills = application.skills.split(', ')
        if any(skill in applicant_skills for skill in job_skills):
            matching_profiles.append(application.applicant)

    context = {
        'job': job,
        'matching_profiles': matching_profiles,
    }

    return render(request, 'matching_profiles.html', context)

@login_required
def changepassPage(request):

    user=request.user

    if request.method =="POST":
        oldpass=request.POST.get("oldpass")
        newpass=request.POST.get("newpass")
        confirmpass=request.POST.get("confirmpass")

        if not check_password(oldpass,user.password):
            messages.error(request,"Current password is wrong")
            return redirect("changepassPage")
        if newpass!= confirmpass:
            messages.error(request,"New password and confirm password are not same.")
            return redirect("changepassPage")
        else:
            user.set_password(confirmpass)
            user.save()
            return redirect("profilePage")

    return render(request,"changepass.html")








def skill_matching_page(request):
    if request.user.user_type == 'recruiter':
        # For recruiters, you might want to show a list of job seekers
        job_seekers = Jobseeker_Profile.objects.all()
        context = {'job_seekers': job_seekers}
    elif request.user.user_type == 'jobseeker':
        # For job seekers, you might want to show a list of jobs matching their skills
        job_seeker_profile = request.user.jobseekerprofile
        job_matching_skills = job_model.objects.filter(Qualifications__icontains=job_seeker_profile.skils)
        context = {'job_matching_skills': job_matching_skills}

    return render(request, 'skill_matching_page.html', context)




def logoutPage(request):
    logout(request)
    return redirect("singinPage")