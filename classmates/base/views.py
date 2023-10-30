from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib import messages

# def registerPage(request):

# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, "User does not exist")

#     context = {}
#     return render(request, 'base/login_registration.html', context)

# def logoutApp(request):


def home(request):
    major = request.GET.get('major') if request.GET.get(
        'major') != None else ''

    class_name = request.GET.get('class') if request.GET.get(
        'class') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=major) & Q(name__icontains=class_name))

    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        # print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
