import cv2
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cap = cv2.VideoCapture(0)
model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True:
    ret, photo = cap.read()
    faces = model.detectMultiScale(photo)
    if len(faces) == 0:
        pass
    else:
        
        x1 = faces[0][0]
        y1 = faces[0][1]
        x2 = x1 + faces[0][2]
        y2 = y1 + faces[0][3]
        aphoto = cv2.rectangle(photo, (x1,y1), (x2, y2), [255, 0, 0], 2)
        #crop_photo = photo[x1:x2, y1:y2]
        cv2.imwrite("detect.jpg", aphoto)
        cv2.imshow("face-photo", aphoto)
        if cv2.waitKey(10) == 13:
            break
cv2.destroyAllWindows()
cap.release()

#Mail
subject = "Security Alert"
body = "This is an email with the image who's detect in the security camera"
sender_email = "sender@gmail.com"
receiver_email = "reciever@gmail.com"
password = input("Type your password and press enter:")

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "detect.jpg"  # In same directory as script

# Open file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
