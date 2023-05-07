from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from media_app.models import User, Post
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    page_name="index.html"
    data = {
        "post_list" : Post.objects.all().order_by('-created_at')
    }
    return render(request, page_name, data)

def sign_up(request):
    page_name = "sign_up.html"
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, page_name, {"error": True, "error_msg": "Username already taken"})
        if User.objects.filter(email=email).exists():
            return render(request, page_name, {"error": True, "error_msg": "Email already taken"})
        user = User.objects.create_user(username=username, email=email, password=password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('profile_settings')
        else:
            return render(request, page_name, {"error": True, "error_msg": "Some error occurred"})
    else: # GET METHOD
        return render(request, page_name)
        
def sign_in(request):
    page_name = "sign_in.html"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('profile_settings')            
        else:
            return render(request, page_name, {"error": True, "error_msg": "Some error occurred"})
    else:
        return render(request, page_name)
    
@login_required(login_url='sign_in')
def sign_out(request):
    auth.logout(request)
    return redirect('sign_up')            
    
@login_required(login_url='sign_in')
def profile_settings(request):
    page_name = "profile_settings.html"
    data = {
        "id": request.user.id,
        "email": request.user.email,
        "username": request.user.username
    }
    return render(request, page_name, data)

@login_required(login_url='sign_in')
def add_post(request):
    user = request.user
    caption = request.POST['caption']
    Post.objects.create(user=user, caption=caption)
    return redirect('index')


    
        
