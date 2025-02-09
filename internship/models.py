from core.models import BaseModel
from django.db import models


class InternshipApplication(BaseModel):
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    linkedin = models.URLField(max_length=255)
    skill = models.CharField(max_length=255)
    experience = models.TextField()
    github_link= models.URLField(max_length=255, default="")
    about_skill = models.TextField()
    certificate = models.FileField(upload_to='certificates/', max_length=500, blank=True, null=True)
    commitment = models.BooleanField()
    birthdate = models.DateField()


    def __str__(self):
        return self.full_name
