from django.urls import path, include

from newzz.crawler import views
from rest_framework.routers import DefaultRouter

routes = DefaultRouter()
routes.register("interests",views.InterestViewSet,"interests")
app_name = "crawler"
urlpatterns = [
    path("api/v1/",include(routes.urls))
]
