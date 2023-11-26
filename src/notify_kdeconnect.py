import cv2 as cv
import datetime
import subprocess
import time

def send_kdeconnect_notification(frame, speed, device_id):
    # Get the current time
    now = datetime.datetime.now()

    # Convert the time to a string
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # Create a text string with the time and speed
    text_string = f'Time: {time_string}\nSpeed: {speed} km/h\n'

    # Write the text on the frame
    y0, dy = 50, 30
    for i, line in enumerate(text_string.split('\n')):
        y = y0 + i*dy
        cv.putText(frame, line, (50, y ), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Save the frame as an image file with a unique filename
    image_filename = f'speed-alert_{now.strftime("%Y%m%d%H%M%S")}.jpg'
    cv.imwrite(image_filename, frame)

    # Send the image file
    subprocess.run(['kdeconnect-cli', '-d', device_id, '--share', image_filename])

    # Send a ping
    subprocess.run(['kdeconnect-cli', '-d', device_id, '--ping-msg', text_string])

