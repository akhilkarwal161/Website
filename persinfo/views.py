# persinfo/views.py
from django.shortcuts import render
from .models import Project, Skill, ContactMessage # Import your models

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
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation (you'd add more robust validation in a real app)
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            # You might want to redirect to a 'thank you' page or show a success message
            return render(request, 'persinfo/contact.html', {'success_message': 'Your message has been sent!', 'page_title': 'Contact - Akhil Karwal Portfolio'})
        else:
            return render(request, 'persinfo/contact.html', {'error_message': 'Please fill in all required fields.', 'page_title': 'Contact - Akhil Karwal Portfolio'})
    return render(request, 'persinfo/contact.html', {'page_title': 'Contact - Akhil Karwal Portfolio'})

