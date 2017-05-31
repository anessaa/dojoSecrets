from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from bcrypt import hashpw, gensalt
import bcrypt
from .models import User, Secret, Like
from django.db.models import Count

def index(request):
    context = {
    "users" : User.objects.all()
    }
    print context
    return render(request, 'dojo_app/index.html')

def validate(request):
    if request.method == "POST":
        errors = User.objects.validate(request)
        if (errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/')
        else:
            # request.session['first_name']=request.POST['first_name']
            hashed_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pass)
            return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['login_email'])
        hashed_pass = bcrypt.hashpw(request.POST['login_password'].encode(), user[0].password.encode())
        if user:
            user = user[0]
            if user.password == hashed_pass:
                request.session['user_id'] = user.id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Email and password are incorrect.')
                return redirect('/')
        else:
            messages.error(request, 'Email not registered')
            return redirect('/')

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')

    user = User.objects.get(pk=user_id)

    list_of_my_like_ids = Like.objects.filter(user=user).values_list('secret__id', flat=True)
    secrets = Secret.objects.all().annotate(Count("like")).order_by("-created_at").values()[:5]

    for secret in secrets:
        print secret
        if secret['id'] in list_of_my_like_ids:
            secret['already_liked'] = True
        else:
            secret['already_like'] = False

    context = {
        "user": user,
        "secrets": secrets
    }
    return render(request, 'dojo_app/dashboard.html', context)
def create_secret(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)

    Secret.objects.create(content=request.POST['content'], user=user)
    return redirect('/dashboard')
def popular_secrets(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    list_of_my_like_ids = Like.objects.filter(user=user).values_list('secret__id', flat=True)

    secrets = Secret.objects.all().annotate(Count("like")).order_by("-like__count").values()
    for secret in secrets:
        print secret
        # if secret['id'] in list_of_my_like_ids:
        #     secret['already_liked'] = True
        # else:
        #     secret['already_like'] = False
    context = {
        'user': user,
        'secrets': secrets,
    }
    return render(request, 'dojo_app/secrets.html', context)



def like(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    secret = Secret.objects.get(pk=id)
    check_likes = Like.objects.filter(user=user, secret=secret)
    if not check_likes:
        Like.objects.create(user=user, secret=secret)
    return redirect('/dashboard')

def delete(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    Secret.objects.get(pk=id).delete()

    return redirect('/dashboard')
def logout(request):
    del request.session['user_id']
    return redirect('/')
