from django.urls import path, include
from django.views.generic import TemplateView
from. import views
from app_smart.API.viewsets import CreateUserAPIViewSet, SensorViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter 
from app_smart.views import CSVUploadView, process_csv_upload
from app_smart.API.filters import (
    SensorFilterView,
    TemperaturaFilterView,
    UmidadeFilterView,
    LuminosidadeFilterView, 
    ContadorFilterView
)
from app_smart.API.viewsets import(
    CreateUserAPIViewSet,
    SensorViewSet, 
    SensorFilter,
    TemperaturaDataViewSet,
    UmidadeDataViewSet,
    LuminosidadeDataView,
    ContadorDataViewSet
)

router = DefaultRouter()
router.register(r'sensores', SensorViewSet)
router.register(r'temperatura', TemperaturaDataViewSet)
router.register(r'umidade', UmidadeDataViewSet)
router.register(r'luminosidade', LuminosidadeDataView)
router.register(r'contador', ContadorDataViewSet)

# router = DefaultRouter()
# router.register(r'sensors', SensorViewSet)
# router.register(r'upload-csv', CSVUploadViewSet, basename='upload-csv')



urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('api/create_user/', CreateUserAPIViewSet.as_view(), name='create_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('process-upload/', process_csv_upload, name='process-upload'),
    path('api/sensor_filter/', SensorFilterView.as_view(), name='sensor_filter'),
    path('api/Temperatura_filter/', TemperaturaFilterView.as_view(), name='temperatura_filter'),
    path('api/umidade_filter/', UmidadeFilterView.as_view(), name='umidade_filter'),
    path('api/luminosidade_filter/', LuminosidadeFilterView.as_view(), name='luminosidade_filter'),
    path('api/contador_filter/', ContadorFilterView.as_view(), name='contador_filter'),
    path('api/process-upload/', views.process_upload, name='process_upload'),
]