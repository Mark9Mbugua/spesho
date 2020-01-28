from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls

from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

schema_view = get_schema_view(
    title='A Different API',
    renderer_classes=[CoreJSONRenderer]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/specials/', include('specials.urls'), name='specials'),
    path('api/v1/comments/', include('comments.urls'), name='comments'),
    path('api/v1/accounts/', include('accounts.urls'), name='accounts'),
    path('api/v1/votes/', include('votes.urls'), name='votes'),
    path('', schema_view, name="docs"),
    path('api/v1/accounts/login', obtain_jwt_token),
    path('api/v1/refresh/token/', refresh_jwt_token),
    path('docs/', include_docs_urls(title='My API title')),
    path('api/auth-jwt-verify/', verify_jwt_token)
]
 