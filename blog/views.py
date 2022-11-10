from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from .models import Post


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                post = Post(title=title, description=description)
                post.save()
        else:
            form = PostForm()
        return render(request, 'blog/add_post.html', {'form': form})
    else:
        HttpResponseRedirect('user_login')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
        else:
            post = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=post)
        return render(request, 'blog/update_post.html', {'form': form})
    else:
        HttpResponseRedirect('user_login')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(pk =id)
            post.delete()
        return HttpResponseRedirect('dashboard')
    else:
        return HttpResponseRedirect('login')


def home_page(request):
    posts = Post.objects.all()
    return render(request, "blog/home.html", {'posts': posts})


def about_page(request):
    return render(request, "blog/about.html")


def contact_page(request):
    return render(request, "blog/contact.html")


def dashboard_page(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:

        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, "blog/dashboard.html", {'posts': posts, 'fullname': full_name, 'groups': groups})
    else:
        return HttpResponseRedirect('login')


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "User logged in Successfully")
                    return HttpResponseRedirect('dashboard')
        else:
            form = LoginForm()
        return render(request, "blog/login.html", {'form': form})
    else:
        return HttpResponseRedirect('dashboard')


def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulation")
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, "blog/signup.html", {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('home')
