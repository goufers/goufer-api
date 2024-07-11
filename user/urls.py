from django.urls import path 
from . import views, password_reset_views
from rest_framework import routers

urlpatterns = [
    #path('register/', views.RegisterUserView.as_view(), name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password_reset/', password_reset_views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uid>/<token>/', password_reset_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('toggle-available/', views.ToggleAvailability, name='toggle_available'),
    path('me/', views.CurrentUserView.as_view(), name='logged_in_gofer'),
]

router = routers.DefaultRouter()
router.register('register', views.RegisterUserView)

urlpatterns = urlpatterns + router.urls