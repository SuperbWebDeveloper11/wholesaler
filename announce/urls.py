from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_for_announces as announces_views
from .views import views_for_categories as categories_views
from .views import views_for_comments as comment_views


app_name = 'announce'

urlpatterns = [

    # announces urls 
    path('', announces_views.AnnounceList.as_view(), name='announce_list'),
    path('add/', announces_views.AnnounceCreate.as_view(), name='announce_add'),
    path('<int:pk>/detail/', announces_views.AnnounceDetail.as_view(), name='announce_detail'),
    path('<int:pk>/update/', announces_views.AnnounceUpdate.as_view(), name='announce_update'),
    path('<int:pk>/delete/', announces_views.AnnounceDelete.as_view(), name='announce_delete'),


    # categories urls 
    path('category/', categories_views.CategoryList.as_view(), name='category_list'),
    path('category/add/', categories_views.CategoryCreate.as_view(), name='category_add'),
    path('category/<int:pk>/detail/', categories_views.CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update/', categories_views.CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', categories_views.CategoryDelete.as_view(), name='category_delete'),


    ####################### urls for creating comments with jQuery #######################
    # comments urls 
    path('<int:pk>/comments/', comment_views.CommentList.as_view(), name='comment_list'),
    path('<int:pk>/comments/add/', comment_views.CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/comments/<int:comment_pk>/update/', comment_views.CommentUpdate.as_view(), name='comment_update'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', comment_views.CommentDelete.as_view(), name='comment_delete'),


]

# urlpatterns = format_suffix_patterns(urlpatterns)

