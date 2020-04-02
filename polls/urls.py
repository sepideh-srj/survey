from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:num>/index/', views.index, name='index'),
    path('<int:question_id>/', views.vote, name='vote'),
    path('<int:question_id>/<int:num>', views.vote, name='vote'),
    path('end/', views.end, name='end'),
    # path('<int:question_id>/returnBlend', views.returnBlend, name='returnBlend')
]