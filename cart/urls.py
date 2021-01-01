from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('download/', views.CartDownload.as_view(), name='cart_download'),
    path('add/<int:announce_id>/', views.CartAdd.as_view(), name='cart_add'),
    path('remove/<int:announce_id>/', views.CartRemove.as_view(), name='cart_remove'),
]

