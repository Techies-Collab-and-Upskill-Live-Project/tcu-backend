from core.models import BaseModel
from django.db import models
from cloudinary.models import CloudinaryField


class InternshipApplication(BaseModel):
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    skill = models.CharField(max_length=255)
    experience = models.TextField()
    github_link= models.CharField(max_length=255, default="")
    about_skill = models.TextField()
    certificate = CloudinaryField('certificate', folder="certificates/", blank=True, null=True)
    commitment = models.BooleanField()
    birthdate = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.full_name
    
    @property
    def certificate_url(self):
        """Returns the complete URL with proper extension"""
        if not self.certificate:
            return None
            
        if isinstance(self.certificate, str):
            return self.certificate
            
        # Handle CloudinaryResource case
        url = self.certificate.url
        if not url.endswith('.pdf'):
            url += '.pdf'
        return url
