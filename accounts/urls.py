from django.urls import path
from .import views


urlpatterns=[
  #Registration
  path('register/',views.register,name='register'),
  path('login/',views.login,name='login'),
  path('logout/',views.logout,name='logout'),
  path('home1', views.home1, name='home1'),
  path('register/otp/<str:uid>/', views.otpVerify, name='otp'),
  path('resend-otp',views.resend_otp,name="resend_otp"),

  #login
  path('otpVerify-login/', views.otpVerify_login, name='otpVerify_login'),
  path('resend-otp-login',views.resend_otp_login,name="resend_otp_login"),
  path('dashboard/',views.dashboard,name='dashboard'),
  path('login-admin',views.login_admin,name="login_admin"),
  path('dashboard-admin',views.dashboard_admin,name="dashboard_admin"),
  path('logout-admin',views.logout_admin,name="logout_admin"),
  
  #admin user management
  path('users-list',views.users_list,name="users_list"),
  path('toggle-user-status/<int:user_id>/',views.toggle_user_status,name="toggle_user_status"),

  #admin category management
  path('category-list/',views.category_list,name="category_list"),
  path('category-add',views.category_add,name="category_add"),
  path('category-update/<int:category_id>', views.category_update, name="category_update"),
  path('category-delete/<int:id>/', views.category_delete, name="category_delete"),

  #admin product management
  path('product-list', views.product_list, name="product_list"),
  path('product-add', views.product_add, name="product_add"),
  path('product-update/<int:product_id>', views.product_update, name="product_update"),
  path('product-delete/<slug:id>', views.product_delete, name="product_delete"),

  #admin variant management
  path('variant-list', views.variant_list, name="variant_list"),
  path('variant-add', views.variant_add, name='variant_add'),
  path('variant-update/<int:variant_id>', views.variant_update, name="variant_update"),
  path('variant-delete/<int:variant_id>', views.variant_delete, name="variant_delete"),
  
  #profile and order management
  path('my-orders/',views.my_orders,name="my_orders"),
  path('edit_profile/',views.edit_profile,name="edit_profile"),
  path('change-password/',views.change_password,name="change_password"),
  path('order-detail/<int:order_id>/',views.order_detail,name="order_detail"),
  path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
  path('address-list/', views.address_list, name='address_list'),
  path('order-list-admin', views.order_list_admin, name="order_list_admin"),
  path('change-order-status/<int:order_id>/', views.change_order_status, name='change_order_status'),
  path('cancel-order2/<int:order_id>/', views.cancel_order2, name='cancel_order2'),
  path('return-order/<int:order_id>/', views.return_order, name='return_order'),
  path('forgot-password/',views.forgot_password,name="forgot_password"),

]


