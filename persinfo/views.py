# persinfo/views.py
from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, ContactMessage # Import your models
from .forms import ContactForm

def home_view(request):
    # Example: Fetch some data to display on the homepage
    projects = Project.objects.all().order_by('-created_at')[:3] # Get latest 3 projects
    skills = Skill.objects.all().order_by('name')
    context = {
        'projects': projects,
        'skills': skills,
        'page_title': 'Home - Akhil Karwal Portfolio'
    }
    return render(request, 'persinfo/home.html', context)

def projects_view(request):
    all_projects = Project.objects.all().order_by('-created_at')
    context = {
        'all_projects': all_projects,
        'page_title': 'My Projects - Akhil Karwal Portfolio'
    }
    return render(request, 'persinfo/projects.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'persinfo/contact.html', {'success_message': 'Your message has been sent!', 'page_title': 'Contact - Akhil Karwal Portfolio'})
        else:
            # If honeypot is filled, it's a bot! Return fake success to stop them trying other fields.
            errors_flat = [error for error_list in form.errors.values() for error in error_list]
            if "Spam detected." in errors_flat:
                return render(request, 'persinfo/contact.html', {'success_message': 'Your message has been sent!', 'page_title': 'Contact - Akhil Karwal Portfolio'})
            
            return render(request, 'persinfo/contact.html', {'error_message': 'Please fill in all required fields correctly.', 'page_title': 'Contact - Akhil Karwal Portfolio'})
    return render(request, 'persinfo/contact.html', {'page_title': 'Contact - Akhil Karwal Portfolio'})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Get previous and next projects based on creation date for navigation.
    # Note: 'prev' is the newer project, 'next' is the older one due to ordering.
    prev_project = Project.objects.filter(
        created_at__gt=project.created_at).order_by('created_at').first()
    next_project = Project.objects.filter(
        created_at__lt=project.created_at).order_by('-created_at').first()

    context = {
        'project': project,
        'prev_project': prev_project,
        'next_project': next_project,
        'page_title': f"{project.title} - Project Details"
    }
    return render(request, 'persinfo/project.html', context)
