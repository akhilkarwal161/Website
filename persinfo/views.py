# persinfo/views.py
import json
import os
import logging
import requests
from django.shortcuts import render, Http404
from django.conf import settings
from .forms import ContactForm

logger = logging.getLogger(__name__)

def send_whatsapp_notification(name, email, subject, message):
    """Sends a WhatsApp notification via Green API."""
    id_instance = os.getenv('GREEN_API_ID')
    api_token = os.getenv('GREEN_API_TOKEN')
    target_phone = os.getenv('TARGET_PHONE')

    if not all([id_instance, api_token, target_phone]):
        logger.warning("WhatsApp notification skipped: Missing Green API credentials.")
        return

    url = f"https://api.green-api.com/waInstance{id_instance}/sendMessage/{api_token}"
    
    # Format message for WhatsApp
    whatsapp_text = (
        f"📩 *New Contact Form Submission*\n\n"
        f"*Name:* {name}\n"
        f"*Email:* {email}\n"
        f"*Subject:* {subject or 'No Subject'}\n\n"
        f"*Message:*\n{message}"
    )

    payload = {
        "chatId": f"{target_phone}@c.us",
        "message": whatsapp_text
    }
    
    try:
        # Increased timeout to 15s for WhatsApp delivery
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        logger.info("WhatsApp notification sent successfully.")
    except Exception as e:
        logger.error("Failed to send WhatsApp notification: %s", e)

def load_portfolio_data():
    """Reads projects and skills data dynamically from JSON file inside repository to avoid idle DB hosting costs."""
    json_path = os.path.join(settings.BASE_DIR, 'persinfo', 'portfolio_data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error("Failed to load portfolio JSON: %s", e)
        return {'projects': [], 'skills': []}

def home_view(request):
    data = load_portfolio_data()
    # Fetch first 3 projects
    projects = data.get('projects', [])[:3]
    skills = data.get('skills', [])
    # Sort skills by name
    skills = sorted(skills, key=lambda x: x.get('name', '').lower())
    
    context = {
        'projects': projects,
        'skills': skills,
        'page_title': 'Home - Akhil Karwal Portfolio'
    }
    return render(request, 'persinfo/home.html', context)

def projects_view(request):
    data = load_portfolio_data()
    all_projects = data.get('projects', [])
    context = {
        'all_projects': all_projects,
        'page_title': 'My Projects - Akhil Karwal Portfolio'
    }
    return render(request, 'persinfo/projects.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            
            # Send WhatsApp Notification via Green API
            send_whatsapp_notification(
                message_obj.name, 
                message_obj.email, 
                message_obj.subject, 
                message_obj.message
            )
            
            # Print to standard output so messages are permanently stored in Google Cloud Logging (100% Free!)
            print(f"\n[CONTACT_MESSAGE] Received submission:")
            print(f"Name: {message_obj.name}")
            print(f"Email: {message_obj.email}")
            print(f"Subject: {message_obj.subject}")
            print(f"Message: {message_obj.message}\n")
            
            return render(request, 'persinfo/contact.html', {
                'success_message': 'Your message has been sent successfully!', 
                'page_title': 'Contact - Akhil Karwal Portfolio'
            })
        else:
            # If honeypot is filled, it's a bot! Return fake success to stop them trying other fields.
            errors_flat = [error for error_list in form.errors.values() for error in error_list]
            if "Spam detected." in errors_flat:
                return render(request, 'persinfo/contact.html', {
                    'success_message': 'Your message has been sent successfully!', 
                    'page_title': 'Contact - Akhil Karwal Portfolio'
                })
            
            return render(request, 'persinfo/contact.html', {
                'error_message': 'Please fill in all required fields correctly.', 
                'page_title': 'Contact - Akhil Karwal Portfolio'
            })
    return render(request, 'persinfo/contact.html', {'page_title': 'Contact - Akhil Karwal Portfolio'})

def project_detail(request, project_id):
    data = load_portfolio_data()
    projects = data.get('projects', [])
    
    # Find active project by ID
    project = None
    project_idx = -1
    for idx, p in enumerate(projects):
        if int(p.get('id', 0)) == int(project_id):
            project = p
            project_idx = idx
            break
            
    if not project:
        raise Http404("Project not found")
        
    # Get previous and next projects based on list navigation (safe bounds check)
    prev_project = projects[project_idx - 1] if project_idx > 0 else None
    next_project = projects[project_idx + 1] if project_idx < len(projects) - 1 else None
    
    context = {
        'project': project,
        'prev_project': prev_project,
        'next_project': next_project,
        'page_title': f"{project.get('title')} - Project Details"
    }
    return render(request, 'persinfo/project.html', context)
