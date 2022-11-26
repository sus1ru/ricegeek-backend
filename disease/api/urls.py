from django.urls import path
from disease.api.views import Diseases, DiseasesDetailAV

urlpatterns = [
    path('list/', Diseases.as_view(), name='disease-list'),
    path('<int:pk>/', DiseasesDetailAV.as_view(), name='disease-detail'),
]