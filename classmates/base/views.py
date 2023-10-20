from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'abc'},
#     {'id': 2, 'name': 'jkl'},
#     {'id': 3, 'name': 'xcv'},
# ]


def home(request):
    major = request.GET.get('major') if request.GET.get(
        'major') != None else ''

    class_name = request.GET.get('class') if request.GET.get(
        'class') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=major) & Q(name__icontains=class_name))

    topics = Topic.objects.all()
    print(topics)

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
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
