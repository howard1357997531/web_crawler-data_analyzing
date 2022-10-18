from django.urls import path, include
from . import views, data_analyzing_views, littlegame_views

urlpatterns = [
    path('', views.home, name='home'),

    # crawler
    path('apple_news/', views.apple_news, name='apple_news'),
    path('get_url', views.get_url, name='get_url'),
    path('yahoo_movie/', views.yahoo_movie, name='yahoo_movie'),
    path('ibon/', views.ibon, name='ibon'),
    path('get_city/', views.get_city, name='get_city'),
    path('taiwan_railway/', views.taiwan_railway, name='taiwan_railway'),
    path('get_taiwan_railway_data/', views.get_taiwan_railway_data,
         name='get_taiwan_railway_data'),

    # data_analyzing
    path('covid/', data_analyzing_views.covid, name='covid'),
    path('student_grade/', data_analyzing_views.student_grade, name='student_grade'),
    path('get_grade/', data_analyzing_views.get_grade, name='get_grade'),
    path('get_rank/', data_analyzing_views.get_rank, name='get_rank'),
    path('edit_grade/', data_analyzing_views.edit_grade, name='edit_grade'),
    path('save_grade/<int:pk>/', data_analyzing_views.save_grade, name='save_grade'),
    path('delete_grade/<int:pk>/',
         data_analyzing_views.delete_grade, name='delete_grade'),


    # littlegame
    path('phone', littlegame_views.phone, name='phone'),
    path('lotto/', littlegame_views.lotto, name='lotto'),


]
