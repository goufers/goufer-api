from django.urls import path 
from . import views, password_reset_views, vendor_views, errand_boy_views
from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('send-code/', views.send_code, name='send-code'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('update/', views.UpdateProfile, name='update'),
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password_reset/', password_reset_views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uid>/<token>/', password_reset_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('gofer/', views.create_list_gofer, name='create-list-gofer'),
]

router = SimpleRouter()
router.register('vendor', vendor_views.VendorViewSet, basename='vendor')
router.register('errand-boy', errand_boy_views.ErrandBoyViewset, basename='errand-boy')

urlpatterns += router.urls
