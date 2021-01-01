from django.urls import include, path
from .views import category, mark, store, product
from .views import category_inline, mark_inline, store_inline, product_inline


app_name = 'sale'


urlpatterns = [
    path('formdata/', category.FormData.as_view(), name='form_data'),

    # category urls
    path('category/', category.CategoryList.as_view(), name='category_list'),
    path('category/add/', category.CategoryCreate.as_view(), name='category_add'),
    path('category/<int:pk>/detail/', category.CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update/', category.CategoryUpdate.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', category.CategoryDelete.as_view(), name='category_delete'),

    # mark urls
    path('mark/', mark.MarkList.as_view(), name='mark_list'),
    path('mark/add/', mark.MarkCreate.as_view(), name='mark_add'),
    path('mark/<int:pk>/detail/', mark.MarkDetail.as_view(), name='mark_detail'),
    path('mark/<int:pk>/update/', mark.MarkUpdate.as_view(), name='mark_update'),
    path('mark/<int:pk>/delete/', mark.MarkDelete.as_view(), name='mark_delete'),

    # store urls
    path('store/', store.StoreList.as_view(), name='store_list'),
    path('store/add/', store.StoreCreate.as_view(), name='store_add'),
    path('store/<int:pk>/detail/', store.StoreDetail.as_view(), name='store_detail'),
    path('store/<int:pk>/update/', store.StoreUpdate.as_view(), name='store_update'),
    path('store/<int:pk>/delete/', store.StoreDelete.as_view(), name='store_delete'),

    # product urls
    path('store/<int:store_pk>/product/', product.ProductList.as_view(), name='product_list'),
    path('store/<int:store_pk>/product/add/', product.ProductCreate.as_view(), name='product_add'),
    path('store/<int:store_pk>/product/<int:pk>/detail/', product.ProductDetail.as_view(), name='product_detail'),
    path('store/<int:store_pk>/product/<int:pk>/update/', product.ProductUpdate.as_view(), name='product_update'),
    path('store/<int:store_pk>/product/<int:pk>/delete/', product.ProductDelete.as_view(), name='product_delete'),

    ############################# urls for inline crud ##############################

    # category_inline urls
    path('category/inline/', category_inline.CategoryList.as_view(), name='category_list_inline'),
    path('category/inline/add/', category_inline.CategoryCreate.as_view(), name='category_create_inline'),
    path('category/inline/<int:pk>/detail/', category_inline.CategoryDetail.as_view(), name='category_detail_inline'),
    path('category/inline/<int:pk>/update/', category_inline.CategoryUpdate.as_view(), name='category_update_inline'),
    path('category/inline/<int:pk>/delete/', category_inline.CategoryDelete.as_view(), name='category_delete_inline'),

    # mark_inline urls
    path('mark/inline/', mark_inline.MarkList.as_view(), name='mark_list_inline'),
    path('mark/inline/add/', mark_inline.MarkCreate.as_view(), name='mark_create_inline'),
    path('mark/inline/<int:pk>/detail/', mark_inline.MarkDetail.as_view(), name='mark_detail_inline'),
    path('mark/inline/<int:pk>/update/', mark_inline.MarkUpdate.as_view(), name='mark_update_inline'),
    path('mark/inline/<int:pk>/delete/', mark_inline.MarkDelete.as_view(), name='mark_delete_inline'),

    # store_inline urls
    path('store/inline/', store_inline.StoreList.as_view(), name='store_list_inline'),
    path('store/inline/add/', store_inline.StoreCreate.as_view(), name='store_create_inline'),
    path('store/inline/<int:pk>/detail/', store_inline.StoreDetail.as_view(), name='store_detail_inline'),
    path('store/inline/<int:pk>/update/', store_inline.StoreUpdate.as_view(), name='store_update_inline'),
    path('store/inline/<int:pk>/delete/', store_inline.StoreDelete.as_view(), name='store_delete_inline'),

    # product_inline urls
    path('store/<int:store_pk>/product/inline/', 
            product_inline.ProductList.as_view(), name='product_list_inline'),
    path('store/<int:store_pk>/product/inline/add/', 
            product_inline.ProductCreate.as_view(), name='product_create_inline'),
    path('store/<int:store_pk>/product/inline/<int:pk>/detail/', 
            product_inline.ProductDetail.as_view(), name='product_detail_inline'),
    path('store/<int:store_pk>/product/inline/<int:pk>/update/', 
            product_inline.ProductUpdate.as_view(), name='product_update_inline'),
    path('store/<int:store_pk>/product/inline/<int:pk>/delete/', 
            product_inline.ProductDelete.as_view(), name='product_delete_inline'),

]


