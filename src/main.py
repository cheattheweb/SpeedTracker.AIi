import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from object_tacker import*
import time
from count_fps import *
from sqlite import *
from notify_kdeconnect import *


model=YOLO('../wiegths/yolov8n.pt')

video_path = '../videos/jp_road.mp4'
time_per_frame = calculate_frame_time(video_path)
print("time per fame = ", time_per_frame)


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
#cv2.setMouseCallback('RGB', RGB)

conn = create_connection()
create_table(conn)

cap=cv2.VideoCapture(video_path)


my_file = open("../classes.txt", "r")
class_list = my_file.read().split("\n") 
#print(class_list)

count=0

tracker=Tracker()

cy1=322
cy2=368

offset=6

vh_down={}
counter=[]


vh_up={}
counter1=[]

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    #if count % 2 != 0:
    #    continue
    frame=cv2.resize(frame,(1020, 500))
   

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]
             
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        #print(c)
        if 'car' in c or 'truck' in c or 'bus' in c:
            list.append([x1,y1,x2,y2])
    bbox_id=tracker.update(list)
    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        
        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)

        if cy1<(cy+offset) and cy1 > (cy-offset):
           vh_down[id]= count
           print(count)
        if id in vh_down:
          
           if cy2<(cy+offset) and cy2 > (cy-offset):
             elapsed_time= (count - vh_down[id]) * time_per_frame
             print(elapsed_time)
             if counter.count(id)==0:
                counter.append(id)
                distance = 10 # meters
                a_speed_ms = distance / elapsed_time
                a_speed_kh = a_speed_ms * 3.6
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                cv2.putText(frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                # inset data into database
                if a_speed_kh > 60:

                    is_success, buffer = cv2.imencode(".jpg", frame)
                    if is_success:
                        image_data = np.array(buffer).tostring()
                        data = (time.strftime("%Y-%m-%d %H:%M:%S"), int(a_speed_kh), str(id), image_data)
                        insert_data(conn, data)

                    # send notification
                    notify = f"SpeedTackerAi_{id},_at_{a_speed_kh}_km/h.pdf"
                    send_kdeconnect_notification(frame, a_speed_kh, "a9901dfa_80fd_4073_b56c_f439efcaa841", notify)

        #####going UP#####     
        if cy2<(cy+offset) and cy2 > (cy-offset):
           vh_up[id]=count
           print(count)
        if id in vh_up:

           if cy1<(cy+offset) and cy1 > (cy-offset):
                    elapsed1_time= (count - vh_up[id]) * time_per_frame
                    print(elapsed1_time)
                    if counter1.count(id)==0:
                        counter1.append(id)
                        distance1 = 10 # meters
                        a_speed_ms1 = distance1 / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                        cv2.putText(frame,str(int(a_speed_kh1))+'Km/h',(x4,y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                        if a_speed_kh > 60:

                            is_success, buffer = cv2.imencode(".jpg", frame)
                            if is_success:
                                image_data = np.array(buffer).tostring()
                                data = (time.strftime("%Y-%m-%d %H:%M:%S"), int(a_speed_kh), str(id), image_data)
                                insert_data(conn, data)

                            # send notification
                            send_kdeconnect_notification(frame, a_speed_kh, "a9901dfa_80fd_4073_b56c_f439efcaa841")

           

    cv2.line(frame,(208,cy1),(814,cy1),(255,255,255),1)

    cv2.putText(frame,('L1'),(277,320),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)


    cv2.line(frame,(97,cy2),(927,cy2),(255,255,255),1)
 
    cv2.putText(frame,('L2'),(182,367),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

