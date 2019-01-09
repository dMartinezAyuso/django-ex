from django.conf import settings
from django.urls import path, re_path, include
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from django.conf.urls import url

schema_view = get_schema_view(title='InnerApps API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/docs/', schema_view, name="docs"),
    re_path('api/(?P<version>(v1|v2))/', include('people.urls')),
    re_path('api/rest-auth/', include('rest_auth.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
