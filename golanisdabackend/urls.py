from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    # Root URL
    path('', home, name='home'),

    # Admin panel
    path('admin/', admin.site.urls),

    # API Routes — versioned under /api/v1/ to match the frontend
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/announcements/', include('apps.announcements.urls')),
    path('api/v1/contact/', include('apps.contact.urls')),
    path('api/v1/donations/', include('apps.donations.urls')),
    path('api/v1/events/', include('apps.events.urls')),
    path('api/v1/leadership/', include('apps.leadership.urls')),
    path('api/v1/gallery/', include('apps.gallery.urls')),
    path('api/v1/ministries/', include('apps.ministries.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/sermons/', include('apps.sermons.urls')),
]

# User-uploaded files live on Render's persistent disk. Static assets are served
# by WhiteNoise in production; Django serves them directly during development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
