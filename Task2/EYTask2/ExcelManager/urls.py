from django.urls import path

from . import views

app_name = 'ExcelManager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('<int:Id>/',views.details, name="detail"),
    path('upload_file/', views.upload_file, name='upload'),
]