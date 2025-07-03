from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


'''
In Django's urls.py file, it is responsible for setting up a route for serving media files.
static - helper function from module for adding roots and serving media files
settings.MEDIA_URL - is a setting from the settings.py file that defines the public URL prefix for media files.
MEDIA_ROOT is the path in the server file system where the uploaded media files are physically stored.
'''


# This is necessary so that Django can give away images and other files.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('forum.urls')),  # Needed to connect routes from other applications

    # JWT-routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
