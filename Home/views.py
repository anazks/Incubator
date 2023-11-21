from django.shortcuts import render
import numpy as np
from matplotlib import pyplot as plt
import cv2
import io
import time
from django.http import JsonResponse
from .models import HeartBeatValue
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import HBSerializer

# Create your views here.

def HomePage(request):
    return render(request,"index.html")

def Analyse(request):
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    cap.set(cv2.CAP_PROP_FPS, 30)
    # Video stream (optional, not tested)
    # cap = cv2.VideoCapture("video.mp4")
    # Image crop
    x, y, w, h = 200, 100, 100, 100
    x, y, w, h = 250, 150, 100, 100
    heartbeat_count = 128
    
    heartbeat_values = [0]*heartbeat_count
    heartbeat_times = [time.time()]*heartbeat_count
    # Matplotlib graph surface
    fig = plt.figure()
    ax = fig.add_subplot(111)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        crop_img = img[y:y + h, x:x + w]
        # Update the data
        heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
        heartbeat_times = heartbeat_times[1:] + [time.time()]
        # Draw matplotlib graph to numpy array
        ax.plot(heartbeat_times, heartbeat_values)
        fig.canvas.draw()
        heartbeat = sum(heartbeat_values)/len(heartbeat_values)
        print(sum(heartbeat_values)/len(heartbeat_values))
        try: 
            HBV = HeartBeatValue.objects.get(id = 1)
            HBV.HB = sum(heartbeat_values)/len(heartbeat_values)
            HBV.save()
        except:
            HBV = HeartBeatValue.objects.create(HB = sum(heartbeat_values)/len(heartbeat_values))
            HBV.save()
        
        plot_img_np = np.fromstring(fig.canvas.tostring_rgb(),
                                    dtype=np.uint8, sep='')
        plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
        # Display the frames
        cv2.imshow("Image",frame)
        # print(val)
        cv2.imshow('Crop', crop_img)
        cv2.imshow('Graph', plot_img_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    return Analyse(request)

@api_view(["GET"])
def HB_API(request):
    HB = HeartBeatValue.objects.all()
    serializer = HBSerializer(HB,many=True)
    print(HB)
    return Response(serializer.data) 
    


