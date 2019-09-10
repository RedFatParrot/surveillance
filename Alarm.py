import cv2
import winsound
import datetime

import tkinter as tk
from tkinter import *
''' 
	TO DO:

-Raspberri-pi som kamera source
-Bruke keyboard modulen i stedet for input som prompt
-Tweake tkinter boksen, adde gui start-up
'''
#(br)exit?
def exitPrompt():
	quitWindow = tk.Tk()
	quitWindow.title("Quit?")
	quitWindow.resizable(width=False, height=False)
	quitWindow.geometry("195x50+600+400")
	quitWindow.iconbitmap("Icons\\quitProgram_icon.ico")

	labelText = tk.Label(quitWindow, text="Are you sure you want to quit?")
	labelText.grid(columnspan=1, row=0, sticky=W, padx=10)

	yesButton = tk.Button(quitWindow, text="Yes", command=quit)
	yesButton.grid(column=0, row=1, sticky=W, padx=10)

	noButton = tk.Button(quitWindow, text="No", command=quitWindow.destroy)
	noButton.grid(column=0, row=1, sticky=E)
	
	quitWindow.mainloop()


def startCam():
	#Define the necessary variables
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	video_capture = cv2.VideoCapture(0)
	dateHandler = datetime.datetime.now()
	currentTime = dateHandler.strftime("%H_%M_%S_%d-%m")
	global startWindow

	if startWindow is not None:
		startWindow.destroy() 
		startWindow = None

	while True:
		#Set-up the video frame and the face cascade
		ret, frame = video_capture.read() 
		faces = faceCascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(30,30))

		#Draw a rectangle around the face(if seen)
		#Take a shot of the detected face
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			cv2.imwrite("FacePictures\\faces" + str(currentTime) + ".jpg", frame)

		#Open a window streaming the camera source
		cv2.imshow('Surveillance Camera', frame)

		#As long as there is a face in the frame, alert
		if (len(faces)) > 0:
			#print ("Face detected")
			winsound.Beep(3000, 1000)

		#Update time variables
		dateHandler = datetime.datetime.now()
		currentTime = dateHandler.strftime("%H_%M_%S_%d-%m")

		#Press 'q' to break out of the while loop
		if cv2.waitKey(1) & 0xFF == ord('q'):
			exitPrompt()
			#Stop recording/streaming
			#video_capture.release()
			#Close windows opened by openCV
			#cv2.destroyAllWindows()


def startPrompt():
	global startWindow
	startWindow = tk.Tk()
	startWindow.title("Camera")
	startWindow.resizable(width=False, height=False)
	startWindow.geometry("111x65+600+400")
	startWindow.iconbitmap("Icons\\quitProgram_icon.ico")

	startLabelText = tk.Label(startWindow, text="Surveillance camera")
	startLabelText.grid(columnspan=1, row=0, sticky=W)

	startButton = tk.Button(startWindow, text="Start", command=lambda:startCam())
	startButton.config(widt="4", height="2")
	startButton.grid(column=0, row=1, sticky=W)

	quitButton = tk.Button(startWindow, text="Stop", command=quit)
	quitButton.config(widt="4", height="2")
	quitButton.grid(column=0, row=1, sticky=E)
	
	startWindow.mainloop()


if __name__ == "__main__":	
	startPrompt()