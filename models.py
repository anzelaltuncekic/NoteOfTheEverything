from ftplib import Error
from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RegisteredUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=255,null=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.username

    def register(self):
        return self.save()

class Note(models.Model):
    registereduser = models.ForeignKey(RegisteredUser, null=True, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=255, null=True)
    topics = [
        ('Biology', ' Biology'),
        ('Math', 'Math'),
        ('English', 'English'),
        ('Android Programming', 'Android Programming'),
        ('History', 'History'),
        ('Operating Systems', 'Operating Systems'),
        ('Formations of Modernity','Formations of Modernity'),
        ('Systems Programming', 'Systems Programming'),
        ('Chemistry', 'Chemistry'),
        ('Java', 'Java'),
        ('Database Systems', 'Database Systems'),
        ('Computer Organization', 'Computer Organization'),
        ('Python', 'Python'),
        ('Discrete Mathematics', 'Discrete Mathematics'),
        ('NLP', 'NLP'),
        ('Logic Design', 'Logic Design'),
        ('Linear Algebra', 'Linear Algebra'),
        ('Principles Of Programming Language', 'Principles Of Programming Language'),
        ('Engineering Statistic', 'Engineering Statistic'),
        ('Internet of Things', 'Internet of Things'),
        ('Computer Network', 'Computer Network'),
        ('Other', 'Other'),

    ]
    note_subject = models.CharField(max_length=255,null=True,choices=topics)
    note_description = models.TextField()
    AorC = [
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('C', 'Cancelled'),
    ]

    note_status = models.CharField(choices=AorC , max_length=50, null=True , default='P')
    note_pagenumber = models.DecimalField(decimal_places=0, max_digits=5, null=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    comment_count = models.IntegerField(default=0)
    note_score = models.DecimalField(decimal_places=1, max_digits=2, default=0)


    def str(self):
        return self.note_title

class NoteImages(models.Model):
    image = models.ImageField(null=True, blank=True)
    gallery = models.ForeignKey(Note,null=True,on_delete= models.CASCADE)

    def str(self):
        return self.image

class user_type(models.Model):
    registereduser = models.ForeignKey(RegisteredUser, on_delete=models.SET_NULL, null=True) #on_delete=models.CASCADE olacak
    user_type_choice = (('A', 'Admin'), ('U', 'User'))
    user_type = models.CharField(choices=user_type_choice, max_length=100, null=True)

    def __str__(self):
        return str(self.registereduser.first_name) + ' ' + str(self.registereduser.last_name) + ' (' + str(self.user_type) + ')'

    class Meta:
        verbose_name = 'User Type'
        verbose_name_plural = 'User Types'
        ordering = ['user_type']

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    owner = [
        ('Anonymous', 'Anonymous'),
        ('Username', 'Username'),
    ]
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    registereduser = models.ForeignKey(RegisteredUser, null=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255, blank=True)
    rating = models.IntegerField(default=0)
    comment_owner = models.CharField(max_length=255, null=True, choices=owner)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
