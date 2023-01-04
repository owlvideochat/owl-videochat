from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import *


# Create your views here.
@csrf_exempt
def signup(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]

    usernames = list(User.objects.values_list('username', flat=True))
    if username in usernames:
        return JsonResponse({"status" : 400, "error": "Username is already taken by others!"})
    if len(password)>4:
        if len(username)>4:
            userdata = User(username=username)
            userdata.set_password(password)
            userdata.save()
            return JsonResponse({"status" : 200, "data": "Account Created Succesfully!"})
        else:
            return JsonResponse({"status" : 400, "error": "Username can't be less than 4 characters"})
    else:
        return JsonResponse({"status" : 400, "error": "Password length must be more than 4 characters"})

def get_user_token(user):
    token_instance,  created = Token.objects.get_or_create(user=user)
    return token_instance.key


@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]
    try:
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({ "status" : 400, "error": "There is no account with this email!"})
        if( user.check_password(password)):
            usr_dict = User.objects.filter(username=username).values().first()
            usr_dict.pop("password")
            if user != request.user:
                login(request, user)
                token = get_user_token(user)
                return JsonResponse({"status" : 200,"token": token,"status":"Logged in"})
            else:
                return JsonResponse({"status":200,"message":"User already logged in!"})
        else:
            return JsonResponse({"status":400,"message":"Invalid Login!"})
    except Exception as e:
        return JsonResponse({"status":500,"message":"Something went wrong!"})

@csrf_exempt   
def signout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return JsonResponse({ "status" : 200, "success" : "logout successful"})
    except Exception as e:
        return JsonResponse({ "status" : 400, "error": "Something Went wrong! Please try again later."})
