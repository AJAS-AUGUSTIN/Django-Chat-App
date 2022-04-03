from email import message
from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from chat.models import ChatModel
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
User = get_user_model()

def index(request):
    if request.session.has_key('username'):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'index.html', context={'users':users})
    else:
        return redirect(login)


def chatPage(request, username):
    try:
        user_obj = User.objects.get(username=username)
        users = User.objects.exclude(username=request.user.username)

        if request.user.id > user_obj.id:
            thread_name = f'chat_{request.user.id}-{user_obj.id}'
        else:
            thread_name = f'chat_{user_obj.id}-{request.user.id}'
        message_obj = ChatModel.objects.filter(thread_name=thread_name)
        return render(request, 'main_chat.html', context={'users':users, 'user':user_obj, 'messages':message_obj})
    except ObjectDoesNotExist:
        return HTTPResponse("Exception: Data not found")

def login(request):
    if request.session.has_key('username'):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'index.html', context={'users':users})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = auth.authenticate(username=username, password=password)
            request.session['username'] = True
            auth.login(request, user)
            users = User.objects.exclude(username=request.user.username)
            return render(request, 'index.html', context={'users':users})
        except:
            messages.info(request, 'Invalid Credentials')
            return redirect(login)
    else:
        return render(request, 'login.html')


def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
    auth.logout(request)
    return redirect(login)