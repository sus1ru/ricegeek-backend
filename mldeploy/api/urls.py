from django.urls import path
from mldeploy.api.views import PredictImage

urlpatterns = [
    path('predict/', PredictImage.as_view(), name='predict'), 
]
  