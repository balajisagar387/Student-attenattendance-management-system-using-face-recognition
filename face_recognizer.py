from distutils.command.config import config
from ast import Lambda
from distutils.command.config import config
from logging import exception
from textwrap import fill
from tkinter import*
from tkinter import ttk
from turtle import width
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from attendance import attendance
import numpy as np
from time import strftime
from datetime import datetime


class face_recognizer:
    
 def __init__(self, root):
  self.root = root
  self.root.geometry("1550x790+0+0")
  self.root.title("Student Attendance Management System")
  
  
  title_lbl = Label(self.root, text="FACE RECOGNITION SYSTEM", font=(
      "times new roman", 25, "bold"), bg="white", fg="green")
  title_lbl.place(x=0, y=0, width=1280, height=40)
  
  img_top = Image.open(
      r"college_images\face_detector1.jpg")
  img_top = img_top.resize((620, 600), Image.ANTIALIAS)
  self.photoimgtop = ImageTk.PhotoImage(img_top)
  f_lbl = Label(self.root, image=self.photoimgtop)
  f_lbl.place(x=0, y=40, width=620, height=600)
  
  
  #2nd image
  img_bottom = Image.open(
      r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
  img_bottom = img_bottom.resize((665, 600), Image.ANTIALIAS)
  self.photoimgbottom = ImageTk.PhotoImage(img_bottom)
  f_lbl1 = Label(self.root, image=self.photoimgbottom)
  f_lbl1.place(x=610, y=40, width=665, height=600)
  
  b1 = Button(f_lbl1, text="Face Recognition",command=self.face_reco,  cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkgreen", fg="white")
  b1.place(x=255, y=530, width=160, height=30)
  
  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)

 def backtoMain(self):

     self.root.destroy()
  
  
  #=====================Attendance==============
 def database_atten(self,i,r,n,d):
     conn = mysql.connector.connect(
         host="localhost", user="root", password="balu123", database="student_management")
     my_cursor = conn.cursor()
     name_list=[]
     now = datetime.now()
     dtstring = now.strftime("%H:%M:%S")
     d1 = now.strftime("%d/%m/%Y")
     
     my_cursor.execute("select * from attendance ")
     list = my_cursor.fetchall()
     for entry in list:
         name_list.append(entry[0])
     
     if(i not in name_list) and (r not in name_list):

         query = "insert into attendance(AttendanceID,Roll,Name,Department,Time,Date,Attendance) values(%s,%s,%s,%s,%s,%s,%s)"
     
         my_cursor.execute(query, (i, r, n, d, dtstring, d1,  "Present"))
         
     conn.commit()
     conn.close()
     
         

     
     
     
     

 def mark_attendance(self, i, r, n, d):
     
    with open("attendance_data/attendance.csv", "r+", newline="\n") as f:
        myDataList = f.readlines()
        name_list = []
        for line in myDataList:
             entry = line.split(",")
             name_list.append(entry[0])
        
        if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
             now = datetime.now()
             d1 = now.strftime("%d/%m/%Y")
             dtstring = now.strftime("%H:%M:%S")
             f.writelines(f"\n{i},{r},{n},{d},{dtstring},{d1},Present") 
    
             
             
  
  
#=============== face recognition
 def face_reco(self):
     def draw_boundry(img,classifier,scaleFactor,minNeighbors,color,text,clf):
         
         gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
         features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

         coord=[]
         for (x,y,w,h) in features:
             conn = mysql.connector.connect(
                 host="localhost", user="root", password="balu123", database="student_management")
             my_cursor = conn.cursor()
             my_cursor.execute(
                 "select Student_id from student")
             id = my_cursor.fetchall()
             
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
             id,predict=clf.predict(gray_image[y:y+h,x:x+w])
             confidence=int((100*(1-predict/300)))
             
             
             
             my_cursor.execute(
                 "select Student_id from student where Student_id="+str(id))
             i = my_cursor.fetchone()
             i = "+".join(i)
             
             
             my_cursor.execute(
                 "select Roll from student where Student_id="+str(id))
             r = my_cursor.fetchone()
             r = "+".join(r)
             
             my_cursor.execute(
                 "select Name from student where Student_id="+str(id))
             n = my_cursor.fetchone()
             n = "+".join(n)
             
             my_cursor.execute(
                 "select Dep from student where Student_id="+str(id))
             d = my_cursor.fetchone()
             d = "+".join(d)
             
             
             
             

             if confidence > 75 :
                 cv2.putText(
                     img, f"Id:{i}", (x, y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                 
                 cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),1)
                 cv2.putText(
                     img, f"Name:{n}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                 
                 cv2.putText(
                     img, f"Department:{d}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                 self.mark_attendance(i, r, n, d)
                 self.database_atten(i,r,n,d)
                 
                 
             else:
                 cv2.rectangle(img,(x, y), (x+w, y+h), (0, 0, 255), 1)
                 cv2.putText(
                     img, f"Unknown Face", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                 
             coord=[x,y,w,h]
             
         return coord
     
     
     
     def recognize(img,clf,faceCascade):
         coord=draw_boundry(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
         return img
     
     faceCascade=cv2.CascadeClassifier("face_classifier.xml")
     clf=cv2.face.LBPHFaceRecognizer_create()
     clf.read("classifier.xml")

     video_cap=cv2.VideoCapture(0)
     while True:
         ret,img=video_cap.read()
         img=recognize(img,clf,faceCascade)
         cv2.imshow("welcome To face Recognizer",img)
         
         if cv2.waitKey(1)==13 :
             
             break
     video_cap.release()
     cv2.destroyAllWindows()
         
     
         
                 










if __name__ == "__main__":
    root = Tk()
    obj = face_recognizer(root)
    root.mainloop()