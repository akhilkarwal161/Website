# Website/mainweb/urls.py
from django.contrib import admin
from django.urls import path, include # Import include
from django.conf import settings # For static/media in development
from django.conf.urls.static import static # For static/media in development
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('persinfo.urls')), # Include your app's URLs at the root
    # You can also include them at a specific path, e.g., path('portfolio/', include('persinfo.urls')),
]

urlpatterns += [
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]

# Serve static and media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Custom error handlers
# Django will automatically use these templates if they exist in the root
# of a templates directory and DEBUG is False. Explicitly defining them
# is good practice.
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
