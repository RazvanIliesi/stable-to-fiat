from django.urls import path

from offers import views

urlpatterns = [
    path("add_offer/", views.OffersCreateView.as_view(), name="add-offer"),
    path("offers_list/", views.OffersListView.as_view(), name="offers-list"),
    path("update_offer/<int:pk>", views.OfferUpdateView.as_view(), name="update-offer"),
    path("delete_offer/<int:pk>", views.OfferDeleteView.as_view(), name="delete-offer")

]
