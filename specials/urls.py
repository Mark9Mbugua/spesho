from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    re_path('categories/(?P<pk>[0-9A-Fa-f-]+)', CategoryDetailView.as_view(), name='get_category'),
    re_path('topics/(?P<pk>[0-9A-Fa-f-]+)', SubCategoryListView.as_view(), name='sub-categories'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
