from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # This path is for the Django Admin Panel (e.g., /admin/)
    path('admin/', admin.site.urls),

    # This is the crucial line. It tells Django that any URL starting with 'api/'
    # should be handled by the urls.py file inside your 'api' app.
    path('api/', include('api.urls')),
]
