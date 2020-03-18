
from django.urls import path

from theme import views

app_name='theme'
urlpatterns = [
    path('front_page/', views.front_page, name='front_page'),
    path('upload_picture/',views.upload_picture,name='upload_picture'),
    path('get_upload_path/',views.get_upload_path,name="get_upload_path"),
    path('get_all_carousal_images_ajax/',views.get_all_carousal_images_ajax,name='get_all_carousal_images_ajax'),
    path('activate_carousal/',views.activate_carousal,name='activate_carousal'),
    path('delete_carousal/',views.delete_carousal,name='delete_carousal'),
    path('start_task/',views.start_background_tast,name="start_task"),
    ]