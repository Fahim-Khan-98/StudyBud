from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room,Topic,Message
from django.db.models import Q
from .forms import RoomForm


# static value view
# rooms = [
#     {'id' : 1, 'name': "Let's Learn Python", 'age': 23 },
#     {'id' : 2, 'name': "Let's Learn C#", 'age': 24 },
#     {'id' : 3, 'name': "Let's Learn Cpp", 'age': 25 },
# ]

# def home(request):
#     context={'rooms': rooms}
#     return render(request,'base/home.html',context)

# def room(request, pk):
#     room = None
#     for i in rooms:
#         if i['id'] == int(pk):
#             room = i
#     context = {'room':room}
#     return render(request,'base/room.html', context)


# ****** Database value view
def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q))
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    context={'rooms': rooms, 'topics':topics, 'room_count': room_count}
    return render(request,'base/home.html',context)

def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
          user = request.user,
          room = room,
          body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages': room_messages,
               'participants': participants}
    return render(request,'base/room.html', context)


@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form,}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this post.....")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this post.....")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html',context)


@login_required(login_url='login')
def DeleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this post.....")
    if request.method == 'POST':
        message.delete()
        # return redirect('room', pk=room.id)
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/delete.html',context)


def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
        except:
            messages.error(request, "User does not exists!!!!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User Or Password does not match!!!!")

    context={'page': page}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')

def RegisterPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!!!!!!')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)