from django.urls import include, path
from django_server.apps.analysis.urls import router as analysis_router


urlpatterns = [
    path(r'server_ipscdb_analysis/v1/', include(analysis_router.urls)),
]
