from typing import Dict, Tuple
from django.db import models
import uuid
from datetime import datetime, timedelta
from .storage import delete_clip_oci, create_par
import pytz

# Create your models here.


class ClipQuerySet(models.query.QuerySet):
    def get(self, *args, **kwargs):
        clip = super().get(*args, **kwargs)
        if clip is not None:
            if clip.url_expiration - timedelta(days=1) < datetime.utcnow().astimezone(
                pytz.utc
            ):
                clip.url, clip.url_expiration = create_par(clip.uuid)
                clip.save()

        return clip

    def all(self, *args, **kwargs):
        clips = super().all(*args, **kwargs)
        for clip in clips:
            if clip.url_expiration - timedelta(days=1) < datetime.utcnow().astimezone(
                pytz.utc
            ):
                clip.url, clip.url_expiration = create_par(clip.uuid)
                clip.save()

        return clips


class ClipManager(models.Manager.from_queryset(ClipQuerySet)):
    pass


class Clip(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4().hex)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    url = models.CharField(max_length=200)
    url_expiration = models.DateTimeField("date url expires")
    thumbnail_url = models.CharField(max_length=200)
    view_count = models.IntegerField(default=0)

    VisibilityType = models.TextChoices("Visibility", "PUBLIC HIDDEN PRIVATE")
    visibility = models.CharField(
        choices=VisibilityType.choices, max_length=10, default=VisibilityType.HIDDEN
    )

    objects = ClipManager()

    def save(self, *args, **kwargs) -> None:
        self.created_at = self.created_at or datetime.now()
        self.updated_at = datetime.now()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> Tuple[int, Dict[str, int]]:
        delete_clip_oci(self.uuid)

        return super().delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Like(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField("date created")
