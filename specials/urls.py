from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
