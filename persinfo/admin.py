# persinfo/admin.py
from django.contrib import admin
from .models import Project, Skill, ContactMessage  # Import your models

# Register your models here.
admin.site.register(Project)
admin.site.register(Skill)
# Also register ContactMessage if you want to view submissions
admin.site.register(ContactMessage)
