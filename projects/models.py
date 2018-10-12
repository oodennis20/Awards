from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Avg
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_photo = models.ImageField(upload_to='profiles/',null=True)
    bio = models.CharField(max_length=240, null=True)
    phone = models.PositiveIntegerField(default=0)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        post_save.connect(create_user_profile, sender=User)

    def save_profile(self):
        self.save()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()

        return profile

    @classmethod
    def find_profile(cls,search_term):
        profile = Profile.objects.filter(user__username__icontains=search_term)
        return profile

class Project(models.Model):
    posted_by = models.ForeignKey(User, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100, null=True)
    project_image = models.ImageField(upload_to='projects/',null=True)
    description = models.TextField(null=True)
    project_link = models.TextField(null=True)

    @classmethod
    def get_projects(cls):
        projects = Project.objects.all()
        return projects

class Reviews(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    juror = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='reviews',null=True)
    design = models.IntegerField(choices=RATING_CHOICES,null=True)
    usability = models.IntegerField(choices=RATING_CHOICES,null=True)
    content = models.IntegerField(choices=RATING_CHOICES,null=True)
    comment = models.CharField(max_length=200,null=True)
    average = models.PositiveIntegerField(default=0)

    @classmethod
    def get_reviews(cls):
        reviews = Reviews.objects.all()
        return reviews

    @classmethod
    def get_average(cls):
        usability =Reviews.objects.all().aggregate(Avg('usability'))
        return usability
