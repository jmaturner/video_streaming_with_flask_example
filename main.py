
#!/usr/bin/env python
# File    : pystream.py ; a Flask app to live stream a usb camera in browser 
# Author  : John Turner
# Version : 0.3  March/2016
#/>.


from flask import Flask, render_template, Markup, Response, request, redirect, session
from flask_basicauth import BasicAuth
from camera import VideoCamera
import smtplib
import time


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'passwd'

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def index():
	return render_template('template.html', bodyText="Welcome to my webcam")



@app.route('/video_feed')
def video_feed():
        return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
	

	
if __name__ == '__main__':
	
	app.run(host='0.0.0.0', port=79)
	#the port must be open on your router I used 79 here.
	#use something obscure.. Have a strong password on the pi
	#In your router settings enter local IP of pi with port 79 forwarded.
	#Then visit www.yourdomain.com:79 or your_ip:79
	
	
