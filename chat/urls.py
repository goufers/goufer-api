from django.urls import path


from . import views


urlpatterns = [
    path("", views.frontpage, name="frontpage"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.loginUser, name="login"),
    path("gofers_list/", views.gofers_list, name="gofers_list"),
    path('create-chat-room/<int:gofer_id>/', views.create_chat_room, name='create_chat_room'),
    path('chat-room/<int:room_id>/', views.chat_room, name='chat_room'),
    path("logout/", views.logoutUser, name="logout"),
    
]