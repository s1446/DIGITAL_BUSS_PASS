from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', login_view, name='home'),

    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('', include('students.urls')),
    path('', include('payments.urls')),
    path('', include('adminpanel.urls')),
    path('', include('notifications.urls')),
]


# VERY IMPORTANT FOR MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )