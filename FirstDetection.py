from imageai.Detection import ObjectDetection
import os
import speech_recognition as sr
import pyttsx3
import win32com.client
import cv2
x=[]
y=[]
z=[]
execution_path = os.getcwd()

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
try:
	print("Google Speech Recognition thinks you said " + r.recognize_google(audio))

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
cap = cv2.VideoCapture(0)
while(True):
	ret,frame = cap.read()
	cv2.imshow('frame', frame)
	if(r.recognize_google(audio)=="capture"):
   		out = cv2.imwrite('capture.jpg',frame)
   		cap.release()
   		cv2.destroyAllWindows()
   		break
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "capture.jpg"), output_image_path=os.path.join(execution_path , "analysis.jpg"))

engine = pyttsx3.init()
engine.setProperty('rate',10)
engine.setProperty('volume', 0.9)
for uniqueObject in detections:
	print(uniqueObject["name"], uniqueObject["box_points"])
	if(uniqueObject["box_points"][0]<85):
		
		x.append(uniqueObject["name"])
	elif(uniqueObject["box_points"][0]<170):
		
		y.append(uniqueObject["name"])
	else:
		
		z.append(uniqueObject["name"])
engine.say("objects to your left")
for i in x:
	engine.say(i)
engine.say("objects in your centre")
for i in y:
	engine.say(i)
engine.say("objects to your right")
for i in z:
	engine.say(i)


engine.runAndWait()

