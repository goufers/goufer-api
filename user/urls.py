from django.urls import path 
from . import views, password_reset_views
from rest_framework_nested import routers

urlpatterns = [
    path('logout/', views.logout_user, name='logout-user'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password_reset/', password_reset_views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uid>/<token>/', password_reset_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('toggle-available/', views.ToggleAvailability, name='toggle_available'),
    path('me/', views.CurrentUserRetrieveView.as_view(), name='logged_in_gofer'),
    path('update-profile-picture/', views.UpdateProfilePicture.as_view(), name='profile_picture_update'),
]

router = routers.DefaultRouter()
router.register('register', views.RegisterUserView, basename='register')
router.register('login', views.LoginUserView, basename='login')
router.register('message-posters', views.MessagePosterViewSet, basename='message-poster')
router.register('pro-gofers', views.ProGoferViewSet, basename='pro-gofer')


pro_gofer_router = routers.NestedDefaultRouter(router, 'pro-gofers', lookup='pro_gofer')
pro_gofer_router.register('schedules', views.ScheduleViewSet, basename='pro_gofer_schedules')

router.register('users', views.UsersViewset, basename='users')
profile_picture_router = routers.NestedDefaultRouter(router, 'users', lookup="users")

urlpatterns = urlpatterns + router.urls + pro_gofer_router.urls + profile_picture_router.urls