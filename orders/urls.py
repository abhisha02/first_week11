
from django.urls import path
from .import views

urlpatterns = [
  
    path('place-order/',views.place_order,name="place_order"),
    path('create-address/',views.create_address,name="create_address"),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('make-payments/<int:order_id>/', views.make_payments, name='make_payments'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('create-address2/',views.create_address2,name="create_address2"),
    path('edit-address2/<int:address_id>/', views.edit_address2, name='edit_address2'),
    path('delete-address2/<int:address_id>/', views.delete_address2, name='delete_address2'),
    path('paypal_payment_success/<int:order_id>/', views.paypal_payment_success, name='paypal_payment_success'),
    path('paypal_payment_failed/<int:order_id>/', views.paypal_payment_failed, name='paypal_payment_failed'),
    path('add-money-wallet/', views.add_money_wallet, name='add_money_wallet'),
    path('order-detail2/<int:order_id>/',views.order_detail2,name="order_detail2"),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('weekly-sales-report/', views.weekly_sales_report, name='weekly_sales_report'),
    path('monthly-sales-report/', views.monthly_sales_report, name='monthly_sales_report'),
    path('yearly-sales-report/', views.yearly_sales_report, name='yearly_sales_report'),
    path('sales-report-pdf/', views.sales_report_pdf, name='sales_report_pdf'),
    path('weekly-report-pdf/', views.weekly_report_pdf, name='weekly_report_pdf'),
    path('monthly-report-pdf/', views.monthly_report_pdf, name='monthly_report_pdf'),
    path('yearly-report-pdf/', views.yearly_report_pdf, name='yearly_report_pdf'),
    path('custom-report/', views.custom_report, name='custom_report'),
    path('custom-report-pdf/<str:starting_date>/<str:ending_date>/',views. custom_report_pdf, name='custom_report_pdf'),

] 