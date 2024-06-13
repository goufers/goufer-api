from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('signIn/', views.TokenObtainPair.as_view(), name='get-token'), # Get token pair
    path('logout/', views.logout_user, name='logout-user'),
    #path('gofer/', views.create_list_gofer, name='create-list-gofer'),
]