from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import HttpResponse, redirect, render

from .forms import UploadClipForm, LoginForm, SignupForm
from .models import Clip
from .storage import upload_clip_oci

# Create your views here.


def editor_view(request):
    return render(request, "clips/editor.html")


def index_view(request):
    if request.user.is_anonymous:
        return redirect("explore")

    clips = Clip.objects.filter(user=request.user).all()

    return render(
        request,
        "clips/index.html",
        {"clips": clips, "upload_form": UploadClipForm()},
    )


def detail_view(request, uuid):
    clip = Clip.objects.get(uuid=uuid)
    if clip.visibility == "PRIVATE" and request.user != clip.user:
        return HttpResponseNotFound()

    return render(
        request,
        "clips/detail.html",
        {"clip": clip},
    )


def upload_view(request):
    if request.method == "POST":
        form = UploadClipForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_anonymous:
                return HttpResponse("Must be logged in to upload")

            uuid, url, time_expires = upload_clip_oci(request.FILES["video"].chunks())
            Clip.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"] or "",
                user=request.user,
                uuid=uuid,
                url=url,
                url_expiration=time_expires,
                thumbnail_url="",
                visibility=form.cleaned_data["visibility"],
            )

            return redirect("index")

        return HttpResponse("Invalid form")
    else:
        return HttpResponse("GET")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(
                request, "clips/login.html", {"error": True, "form": LoginForm()}
            )
    else:
        return render(request, "clips/login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("index")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        if password != password_confirm:
            return render(
                request, "clips/signup.html", {"error": True, "form": SignupForm()}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request, "clips/signup.html", {"error": True, "form": SignupForm()}
            )

        user = User.objects.create_user(username, password=password)
        user.save()
        login(request, user)
        return redirect("index")
    else:
        return render(request, "clips/signup.html", {"form": SignupForm()})


def explore_view(request):
    clips = Clip.objects.filter(visibility="PUBLIC").all()
    return render(request, "clips/explore.html", {"clips": clips})


def delete_view(request, uuid):
    clip = Clip.objects.get(uuid=uuid)
    if request.user != clip.user:
        return redirect("index")

    clip.delete()
    return redirect("index")
