from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
 #   path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),

    # path('feedback/',views.feedback,name="feedback"),

    # path('admin-login/login/feedback-details/',views.feedbackdetails,name="details"),
    # path('admin-login/login/order-details/',views.orderdetails,name="orderdet"),
    # path('accounts/login/?next=/feedback-details/',views.feedbackdetails,name="details"),

    # path('accounts/login/?next=/order-details/',views.orderdetails,name="orderdet"),

    path('feedback-submit/',views.feedbacksuccess,name="feedbacksuccess"),

    path('product/', views.product,name="product"),
    path('product/?', views.query,name="query"),

    # path('order/<int:pk>', views.order,name="order"),
    # path('search/order/<int:pk>', views.order,name="order"),
    path('product/order/<int:pk>', views.order,name="order"),
    # path('product/sort/order/<int:pk>', views.order,name="order"),
    # path('product/search/order/<int:pk>', views.order,name="order"),

    # path('ordersuccess/', views.ordersuccess,name="success"),
    # path('product/search/ordersuccess/', views.ordersuccess,name="success"),
    path('product/ordersuccess/', views.ordersuccess,name="success"),
   
    path('product/search/ordersuccess/', views.ordersuccess,name="success"),
    
   
    path('search/',views.search,name="search"),
    path('product/search/',views.search,name="pro-search"),
    

    # path('product/sort/',views.sort,name="sort"),

    path('admin-login/',views.login,name="login"),
    path('admin-login/login/',views.loginsuccess,name="log-success"),
    
    # path('admin-login/login/logout/',views.logout,name="logout"),

    # path('admin-login/feedback-details/',views.feedbackdetails,name="details"),
    path('admin-view/order-details/',views.orderdetails,name="orderdet"),
    path('admin-view/order-details/delivered/<int:pk>/',views.delivered,name="delivered"),
    # path('feedback-details/verified/<int:pk>/',views.verified,name="verified")
]
