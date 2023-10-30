from django.shortcuts import render, redirect
from django.http import JsonResponse

import requests

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone


def ask_chatbot(message):
    url = "https://chatgpt-gpt4-ai-chatbot.p.rapidapi.com/ask"
    payload = { "query": message }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "add your API key here",
        "X-RapidAPI-Host": "chatgpt-gpt4-ai-chatbot.p.rapidapi.com"
        }
    response = requests.post(url, json=payload, headers=headers)
    answer = response.json().get("response")
    return answer


# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        #response = ask_openai(message) #using for openai
        response = ask_chatbot(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()  #save chat into the data base
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user) #if 2 passwords match, system will auto login with this user information 
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')