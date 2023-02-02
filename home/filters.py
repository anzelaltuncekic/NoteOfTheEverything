
import django_filters
from django import forms
from .models import *


class NoteFilter(django_filters.FilterSet):
    class Meta:
        model=Note
        fields = ['note_subject']
