from django.urls import path

from orders import views

urlpatterns = [
    path('offer/<int:offer_id>/sell/', views.SellOrderView.as_view(), name='sell-order'),
    path('offer/<int:offer_id>/buy/', views.BuyOrderView.as_view(), name='buy-order'),

]
