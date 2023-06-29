from django.urls import path
from . import views

urlpatterns = [
    path('routes/', views.getRoutes, name='getRoutes'),
    path('inspections/', views.getInspections, name='getInspections'),
    path('inspections/<str:pk>', views.getInspection, name='getInspection'),
    path('inspections/<str:pk>/update', views.updateInspection, name='updateInspection'),

    path('questions/', views.getQuestions, name='getQuestions'),
    path('postAnswers/', views.postAnswers, name='postAnswers'),
    path('getAnswers/<str:pk>', views.getAnswers, name='getAnswers'),
]
