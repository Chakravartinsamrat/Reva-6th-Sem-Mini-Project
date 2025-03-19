from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process/<int:document_id>/', views.process_document, name='process_document'),
]