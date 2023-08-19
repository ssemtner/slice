from django.shortcuts import render, HttpResponse, redirect
from .forms import UploadClipForm
from .storage import upload_clip_oci
from .models import Clip

# Create your views here.


def index(request):
    return render(
        request,
        "clips/index.html",
        {"clips": Clip.objects.all(), "upload_form": UploadClipForm()},
    )


def detail(request, uuid):
    return render(
        request,
        "clips/detail.html",
        {"clip": Clip.objects.get(uuid=uuid)},
    )


def upload(request):
    if request.method == "POST":
        form = UploadClipForm(request.POST, request.FILES)
        if form.is_valid():
            uuid, url, time_expires = upload_clip_oci(request.FILES["video"].chunks())
            Clip.objects.create(
                title=form.cleaned_data["title"],
                description="",
                user=request.user,
                uuid=uuid,
                url=url,
                url_expiration=time_expires,
                thumbnail_url="",
            )

            return redirect("index")

        return HttpResponse("Invalid form")
    else:
        return HttpResponse("GET")
