from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('collections/',views.collection,name='collections'),
    path('collections/ <str:name>/',views.collectionView,name='collections'),
    path('collections/<str:cname>/<str:pname>/',views.productView,name='product'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('addtocart/',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart,name='cart'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('addtofav/',views.add_to_fav,name='addtofav'),
    path('favorites/',views.fav,name='favorites'),
    path('remove_fav/<str:fid>/',views.remove_fav,name='remove_fav'),
    path('placeorder/',views.place_order,name='place_order'),
    path('orderditem/',views.order,name='orders'),
    path('remove_order/<str:oid>/',views.remove_order,name='remove_order'),
     path('search/', views.search_view, name='search_view'),
    path('order_details/<str:did>/',views.order_details,name='order_details')
  
 
]

