from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    USER=[
        ('recruiter', 'Recruiter'),
        ('jobseeker', 'JobSeeker')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER, max_length=120)
    Profile_picture=models.ImageField(upload_to="media/Profile_pic",null=True)

    def __str__(self):
        return self.username
    

class Recruiter_Profile(models.Model):
    user=models.OneToOneField(Custom_User, on_delete=models.CASCADE,null=True, related_name='recruiterprofile')

    def __str__(self):
        return self.user.display_name


class Jobseeker_Profile(models.Model):
    user=models.OneToOneField(Custom_User, on_delete=models.CASCADE,null=True, related_name='jobseekerprofile')
    resumes=models.FileField(upload_to="media/resumes",null=True)
    skils=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.user.display_name
    


class job_model(models.Model):
    job_title=models.CharField(max_length=100,null=True)
    company_name=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    description=models.TextField()
    company_description=models.TextField(null=True)
    Qualifications=models.CharField(max_length=100,null=True)
    deadline=models.CharField(max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to="media/Profile_Pic",null=True)
    create_at=models.DateTimeField(auto_now_add=True,null=True)
    update_time=models.DateTimeField(auto_now=True,null=True)
    job_creator=models.ForeignKey(Custom_User, on_delete=models.CASCADE)


    def __str__(self):
        return self.company_name
    


class jobapplyModel(models.Model):
    job=models.ForeignKey(job_model,on_delete=models.CASCADE,null=True)
    applicant=models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    skills=models.CharField(max_length=100,null=True)
    apply_resume=models.FileField(upload_to="media/apply_resume",null=True)

    def __str__(self):
        return f"{self.applicant.display_name} Applied for {self.job.job_title}"
    