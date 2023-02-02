from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' ,'first_name' , 'last_name' , 'email' ,'password1' , 'password2' ]

class Share_Note(ModelForm):
    class Meta:
        model = Note
        fields = ['note_title' , 'note_description' , 'note_pagenumber' , 'note_subject']

class Note_Images(ModelForm):
    class Meta:
        model= NoteImages
        fields = ['image']

class ChangeEmailForm(ModelForm):
   class Meta:
      model=RegisteredUser
      fields = ['email']
      widgets = {
         'email': forms.TextInput(attrs={'class': 'form-control'}),
      }

class ChangeUsernameForm(ModelForm):
   class Meta:
      model=RegisteredUser
      fields = ['username']
      widgets = {
         'username': forms.TextInput(attrs={'class': 'form-control'}),
      }

class CommentForm(ModelForm):
    class Meta:
     model=Comment
     fields=['comment','rating','comment_owner']

