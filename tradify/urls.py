from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('charts/', views.charts, name='charts'),
    path('uvolume/', views.uvolume, name='uvolume'),
    path('equity/', views.equity, name='equity'),
    path('help/', views.help, name='help'),
    path('exporttool/', views.exporttool, name='exporttool'),
    path('download/', views.download, name='download'),
]