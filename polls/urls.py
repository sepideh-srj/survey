from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('<int:num>/index/', views.index, name='index'),
    # path('<int:question_id>/', views.vote, name='vote'),
    path('process', views.process, name='process'),
    path('vote/<int:userID>/<int:question_id>', views.vote, name='vote'),
    path('end/<int:userID>', views.end, name='end'),
    # path('<int:question_id>/returnBlend', views.returnBlend, name='returnBlend')
]