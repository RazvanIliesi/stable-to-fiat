from django.urls import path

from orders import views

urlpatterns = [
    path('offer/<int:offer_id>/sell/', views.SellOrderView.as_view(), name='sell-order'),
    path('offer/<int:offer_id>/buy/', views.BuyOrderView.as_view(), name='buy-order'),
    path('success/', views.OrderSuccessView.as_view(), name='order-success'),
    path("oders_list/", views.OrderListView.as_view(), name='order-list'),
    path('orders/change_status/<uuid:order_id>/', views.ChangeOrderStatusView.as_view(), name='change-order-status')

]
