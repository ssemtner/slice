import oci
from uuid import uuid4
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from django.apps import apps

config = oci.config.from_file()
object_store = oci.object_storage.ObjectStorageClient(config)
namespace = object_store.get_namespace().data
bucket = object_store.get_bucket(namespace, "clips-bucket").data


def upload_clip_oci(chunks):
    uuid = uuid4().hex

    upload = object_store.create_multipart_upload(
        namespace,
        bucket.name,
        oci.object_storage.models.CreateMultipartUploadDetails(
            object=uuid, content_type="video/quicktime"
        ),
    ).data

    i = 1
    bigger_chunk = b""
    try:
        while True:
            if len(bigger_chunk) > 5 * 1000 * 1000:  # 5 mb
                object_store.upload_part(
                    namespace, bucket.name, uuid, upload.upload_id, i, bigger_chunk
                ).data
                i += 1
                bigger_chunk = b""
            else:
                bigger_chunk += next(chunks)
    except StopIteration:
        object_store.upload_part(
            namespace, bucket.name, uuid, upload.upload_id, i, bigger_chunk
        ).data

    summary = object_store.list_multipart_upload_parts(
        namespace, bucket.name, uuid, upload.upload_id
    ).data

    object_store.commit_multipart_upload(
        namespace,
        bucket.name,
        uuid,
        upload.upload_id,
        oci.object_storage.models.CommitMultipartUploadDetails(
            parts_to_commit=[
                oci.object_storage.models.CommitMultipartUploadPartDetails(
                    part_num=part.part_number, etag=part.etag
                )
                for part in summary
            ]
        ),
    )

    # Get pre-authenticated request
    req_details = oci.object_storage.models.CreatePreauthenticatedRequestDetails(
        name=uuid,
        object_name=uuid,
        access_type="ObjectRead",
        time_expires=datetime.utcnow() + timedelta(days=30),
    )
    pre_auth_req = object_store.create_preauthenticated_request(
        namespace, bucket.name, req_details
    ).data

    return uuid, pre_auth_req.full_path, pre_auth_req.time_expires


def delete_clip_oci(uuid):
    object_store.delete_object(namespace, bucket.name, uuid)


class RemoveUnusedClips(CronJobBase):
    schedule = Schedule(run_at_times=["03:00"])
    code = "clips.remove_unused_clips"  # a unique code

    def do(self):
        clip_uuids = [clip.uuid for clip in apps.get_model('clips.Clip').objects.all()]

        for obj in object_store.list_objects(namespace, bucket.name).data.objects:
            if obj.name not in clip_uuids:
                object_store.delete_object(namespace, bucket.name, obj.name)
