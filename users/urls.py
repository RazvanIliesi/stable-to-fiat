from django.urls import path

from users import views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view(), name='create-user'),
    path('activate/<uid64>/<token>/', views.activate_user, name='activate'),
    path('profile/<int:pk>/', views.UserProfile.as_view(), name='user-profile'),
    path('profile/edit/<int:pk>/', views.EditProfileView.as_view(), name='edit-profile'),
    path("user_verification/", views.UserVerificationCreateView.as_view(), name="user-verification"),
    path("user_verification_done/", views.UserVerificationDoneView.as_view(), name="user-verification-done"),

]
