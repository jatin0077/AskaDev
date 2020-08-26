from django.contrib import admin
from .models import Question, Tags, Answer

admin.site.register(Question)
admin.site.register(Tags)
admin.site.register(Answer)
