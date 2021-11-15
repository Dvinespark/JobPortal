from django.db import models
from datetime import datetime

now = datetime.now()
folder_path = str(now.strftime('%Y/%m/%d'))
LOGO_PATH = 'logo/' + folder_path
RESUME_PATH = 'resume/' + folder_path
# Create your models here.
STATUS_CHOICES = (
    ('International Students', 'International Students'),
    ('PR / Citizen', 'PR / Citizen')
)
AVAILABILITY_CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time')
)
EMPLOYMENT_TYPE = (
    ('Contract', 'Contract'),
    ('Permanent', 'Permanent')
)


class Employer(models.Model):
    class Meta:
        db_table = "Employer"
    job_title = models.CharField(max_length=250, blank=False, null=False)
    company = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=LOGO_PATH)
    job_description = models.TextField()
    email = models.CharField(max_length=100)
    rate = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES)
    duration = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=30, choices=EMPLOYMENT_TYPE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=30, blank=True, null=True)
    updated_by = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.job_title


class Employees(models.Model):
    class Meta:
        db_table = "Employees"
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100)
    skill = models.CharField(max_length=50, blank=True, null=True)
    experience_year = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES)
    resume = models.FileField(upload_to=RESUME_PATH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=30, blank=True, null=True)
    updated_by = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.email + ' -- ' + str(self.employer)
