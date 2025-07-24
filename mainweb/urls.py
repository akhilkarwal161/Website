# Website/mainweb/urls.py
from django.contrib import admin
from django.urls import path, include # Import include
from django.conf import settings # For static/media in development
from django.conf.urls.static import static # For static/media in development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('persinfo.urls')), # Include your app's URLs at the root
    # You can also include them at a specific path, e.g., path('portfolio/', include('persinfo.urls')),
]

# Serve static and media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

