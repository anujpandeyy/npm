from django.contrib import admin
from django.urls import path
from django.urls.conf import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('members/', include("members.urls")),
    path('project/', include("projects.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)