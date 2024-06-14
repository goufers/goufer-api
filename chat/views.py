from django.contrib.auth import login, logout, authenticate
from user.models import CustomUser, Gofer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F, Q

from .models import Gofer, ChatRoom
from .forms import SignUpForm

def frontpage(request):
    return render(request, "chat/frontpage.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "chat/signup.html", {'form': form})

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect('gofers_list')
        else:
            return JsonResponse({'error': 'Invalid username or password'})
    return render(request, 'chat/login.html')

def logoutUser(request):
    logout(request)
    return redirect('frontpage')

@login_required
def gofers_list(request):
    gofers = Gofer.objects.annotate(order=F('id'))
    users = CustomUser.objects.all()
    user = request.user
    context = {
        'gofers': gofers,
        'users': users,
        'user': user
    }
    try:
        gofer = Gofer.objects.get(user=user.id)
        chat_rooms = ChatRoom.objects.filter(Q(user=user) | Q(gofer=gofer))
        context['chat_rooms'] = chat_rooms
    except Gofer.DoesNotExist:
        chat_rooms = ChatRoom.objects.filter(user=user)
        context['chat_rooms'] = chat_rooms
    return render(request, 'chat/gofers_list.html', context)

@login_required
def create_chat_room(request, gofer_id):
    user = request.user
    gofer = get_object_or_404(Gofer, id=gofer_id)
    
    # Check if a chat room already exists for this user and gofer
    chat_room = ChatRoom.objects.filter(user=user, gofer=gofer).first()
    
    if chat_room:
        # If a chat room already exists, return it
        return redirect('chat_room', room_id=chat_room.id)
    else:
        # If no chat room exists, create a new one
        chat_room = ChatRoom.objects.create(user=user, gofer=gofer)
        return redirect('chat_room', room_id=chat_room.id)

@login_required
def chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    return render(request, 'chat/chat_room.html', {'chat_room': chat_room})
