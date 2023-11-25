import cv2 as cv
import datetime
import subprocess
from fpdf import FPDF

def send_kdeconnect_notification(frame, speed, device_id,time_string):

    # Save the frame as an image file
    image_filename = 'frame.jpg'
    cv.imwrite(image_filename, frame)

    # Get the current time
    now = datetime.datetime.now()

    # Convert the time to a string
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # Create a text file with the time and spee
    text_filename = 'info.txt'
    with open(text_filename, 'w') as f:
        f.write(f'Time: {time_string}\nSpeed: {speed} km/h\n')

    # Create a PDF file with the image and text
    pdf_filename = f'speedTrackerAi.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_filename, x=5, y=8, w=200)
    pdf.set_font('Arial', size=16, style='B')
    with open(text_filename, 'r') as f:
        for line in f:
            pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(pdf_filename)

    # Send the PDF file
    subprocess.run(['kdeconnect-cli', '-d', device_id, '--share', pdf_filename])
