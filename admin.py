from django.contrib import admin

from .models import *

admin.site.register(RegisteredUser)
admin.site.register(Note)
admin.site.register(NoteImages)
admin.site.register(user_type)
admin.site.register(Comment)