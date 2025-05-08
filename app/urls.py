from django.urls import path
from .views import DocumentResultView


urlpatterns = [
    path('upload/', DocumentResultView.upload_document, name='upload_document'),
    path('results/', DocumentResultView.display_results, name='display_results'),
]
