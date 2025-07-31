# persinfo/urls.py
from django.urls import path
from . import views

app_name = 'persinfo' # Namespace for this app's URLs

urlpatterns = [
    path('', views.home_view, name='home'),
    path('projects/', views.projects_view, name='projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact_view, name='contact'),
    # Add more paths as needed for other pages
]
