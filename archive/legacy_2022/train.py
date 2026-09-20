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
import numpy as np


class train:
 def __init__(self, root):
  self.root = root
  self.root.geometry("1550x790+0+0")
  self.root.title("Student Attendance Management System")
  
  
  
  title_lbl = Label(self.root, text="TRAIN DATA SET", font=(
      "times new roman", 25, "bold"), bg="white", fg="red")
  title_lbl.place(x=0, y=0, width=1280, height=40)
  
  
  img_top = Image.open(
      r"college_images\facialrecognition.png")
  img_top = img_top.resize((1275, 300), Image.ANTIALIAS)
  self.photoimgtop = ImageTk.PhotoImage(img_top)
  f_lbl = Label(self.root, image=self.photoimgtop)
  f_lbl.place(x=0, y=40, width=1275, height=300)
  
  img_bottom = Image.open(
      r"college_images\photos.jpg")
  img_bottom = img_bottom.resize((1275, 250), Image.ANTIALIAS)
  self.photoimgbottom = ImageTk.PhotoImage(img_bottom)
  f_lbl = Label(self.root, image=self.photoimgbottom)
  f_lbl.place(x=0, y=380, width=1275, height=250)
  #==================button
  b1 = Button(self.root, text="TRAIN DATA",command=self.train_classifier, cursor="hand2", font=(
      "times new roman", 25, "bold"), bg="red", fg="white")
  b1.place(x=0, y=340, width=1275, height=40)
  
  
  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)

 def backtoMain(self):

     self.root.destroy()

  
 def train_classifier(self):
     data_dir=("data")
     path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
     
     faces=[]
     ids=[]
     conn = mysql.connector.connect(
         host="localhost", user="root", password="balu123", database="student_management")

     my_cursor = conn.cursor()
     my_cursor.execute
     
     for image in path :
         img=Image.open(image).convert('L') # grey scale convert
         imagenp=np.array(img,'uint8')
         
         my_cursor.execute(
             "select Student_id from student")
         student_id = my_cursor.fetchall()
         
         
         
         id=int(os.path.split(image)[1].split('.')[1])
         faces.append(imagenp)
         ids.append(id)
         cv2.imshow("Training",imagenp)
         cv2.waitKey(1)==13
         
     ids=np.array(ids)
     
     #=============== Train classifier
     
     clf = cv2.face.LBPHFaceRecognizer_create()
     clf.train(faces, ids)
     
     clf.write("classifier.xml")
     cv2.destroyAllWindows()
     messagebox.showinfo("Result","Training datasets completed",parent=self.root)
         
























if __name__ == "__main__":
    root = Tk()
    obj = train(root)
    root.mainloop()
