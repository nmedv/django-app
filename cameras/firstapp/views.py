from ast import arg
from asyncio.windows_events import NULL
from ipaddress import ip_network
import threading
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from cameras.settings import HOST, PORT
import cv2


SERVER = "http://" + HOST + ":" + PORT


def index(request):
    return render(request, "index.html")


def gen_frame(addr):
    try: addr = int(addr)
    except: print("error converting addr to int")
    finally: camera = cv2.VideoCapture(addr)

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def video_stream(request):
    addr = request.GET.get("addr", None)
    if addr:
        return StreamingHttpResponse(gen_frame(addr), content_type="multipart/x-mixed-replace;boundary=frame")
    else:
        return HttpResponse("None")


def cameras(request):
    data = {
        "server": SERVER,
        "cam_urls": [
            "0",
            "1",
            "2",
            "rtsp://192.168.0.101:8080/h264_pcm.sdp",
            "rtsp://192.168.0.101:8080/h264_ulaw.sdp",
            "http://192.168.0.101:8080",
            "https://192.168.0.101:8080"
        ]
    }
    return render(request, "cameras.html", data)