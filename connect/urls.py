from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import PatientViewSet, HealthWorkerViewSet, RequestViewSet, CustomAuth

router = routers.DefaultRouter()
router.register('patient', PatientViewSet)
router.register('worker', HealthWorkerViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
  path('', include(router.urls)),
  url(r'^auth/', CustomAuth.as_view()),
]