from django.contrib import admin
from .models import ProgrammingLanguage, UserProfile

admin.site.register(UserProfile)
admin.site.register(ProgrammingLanguage)