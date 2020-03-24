from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.vote, name='vote'),
    path('<int:question_id>/returnBlend', views.returnBlend, name='returnBlend')
]