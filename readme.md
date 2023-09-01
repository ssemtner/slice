# I'm archiving this repository and rewriting slice in nextjs.
As I am moving my focus to UI, django and templates gets less effective, and I'm not in the mood to learn HTMX.

Also, there are much better free hosting options for js based projects.

# Slice

Slice is a simple platform to share short clips to a platform like discord (with embeds).

I was inspired to make this after reaching the discord file size limit when trying to share a clip.

The end goal is to integrate simple video editing tools to make it quicker for me to go from a 5 minute video file to an easily sharable clip.


## Features
- [x] Upload video files
- [x] Multiple visibility options (public, hidden, private)
- [x] Embeds for discord
- [x] Preview video before upload
- [x] Video playback
- [x] Explore page for public videos
- [x] Video trimming
- [ ] Public avaliability
- [ ] Storage limits and autodeletion options
- [ ] Modernize UI
- [ ] User profiles
- [ ] Thumbnail support
- [ ] Multiple file format support

## Technologies
- Python
- Django
- Oracle Cloud Infrastructure Bucket Storage
- Render for free hosting
- Neon for free database


## How videos are stored
When you upload a video it is instantly uploaded to an Oracle Cloud Object Storage Bucket.
Videos are never saved on the server, they are streamed directly from the form to the bucket.
Each video is given a preauthenticated request (par) url that is valid for 30 days.
The par url is automatically regenerated when it is close to expiring.


## How the video preview / future video editing will work
When you add a video to the form, a javascript function saves it to a blob url.
The html video source tag is then set to the blob url.

The planned video editing functionallity will use allow setting a start and end time for the video.
The video will then be sent to an ffmpeg.js web worker to be trimmed.

This method will allow for future editing features to be added in the future.
