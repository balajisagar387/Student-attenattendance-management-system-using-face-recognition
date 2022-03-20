from cgitb import text
from os import times
from time import strftime
from tkinter import*
from tkinter import ttk
import tkinter
from PIL import Image,ImageTk
from student import Student
from train import train
from face_recognizer import face_recognizer
from attendance import attendance
from help import help
from developer import developer
import os


class face_recognization_system:
 def __init__(self,root):
  self.root=root
  self.root.geometry("1550x790+0+0")
  self.root.title("Student Attendance Management System")
  
  img = Image.open(r"college_images\Stanford.jpg")
  img= img.resize((500,130),Image.ANTIALIAS)
  self.photoimg=ImageTk.PhotoImage(img)
  f_lbl=Label(self.root,image=self.photoimg)
  f_lbl.place(x=0,y=0,width=423,height=130)
  
  img1 = Image.open(
      r"college_images\facialrecognition.png")
  img1 = img1.resize((500, 130), Image.ANTIALIAS)
  self.photoimg1 = ImageTk.PhotoImage(img1)
  f_lbl = Label(self.root, image=self.photoimg1)
  f_lbl.place(x=423, y=0, width=430, height=130)
  
  img2 = Image.open(
      r"college_images\u.jpg")
  img2 = img2.resize((500, 130), Image.ANTIALIAS)
  self.photoimg2 = ImageTk.PhotoImage(img2)
  f_lbl = Label(self.root, image=self.photoimg2)
  f_lbl.place(x=850, y=0, width=432, height=130)
  
  
  
   # bg image
  img3 = Image.open(
      r"college_images\wp2551980.jpg")
  img3 = img3.resize((1280, 750), Image.ANTIALIAS)
  self.photoimg3 = ImageTk.PhotoImage(img3)
  bg_img = Label(self.root, image=self.photoimg3)
  bg_img.place(x=0, y=130, width=1280, height=530)
  
  
  
  #lable title
  
  title_lbl=Label(bg_img,text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",font =("times new roman",25,"bold"),bg="white",fg="green")
  title_lbl.place(x=0,y=0,width=1280,height=40)
  
#==========time
  def time():
      string=strftime('%H:%M:%S %p')
      lbl.config(text=string)
      lbl.after(1000,time)
      
  lbl = Label(title_lbl, font=("times new roman",
              14, "bold"), bg="white", fg="blue")
  lbl.place(x=10,y=0,width=100,height=40)
  time()
  
  
  
  
  
  
  
  
  
  
  #student button
  img4 = Image.open(
      r"college_images\gettyimages-1022573162.jpg")
  img4 = img4.resize((150, 150), Image.ANTIALIAS)
  self.photoimg4 = ImageTk.PhotoImage(img4)
  b1=Button(bg_img,image=self.photoimg4,command=self.student_details ,cursor="hand2")
  b1.place(x=250,y=90,width=150,height=150)
  
  b1_1 = Button(bg_img, text="Student Details", command=self.student_details , cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_1.place(x=250, y=240, width=150, height=30)
  
  
  #Detect Face button
  img5 = Image.open(
      r"college_images\face_detector1.jpg")
  img5 = img5.resize((150, 150), Image.ANTIALIAS)
  self.photoimg5 = ImageTk.PhotoImage(img5)
  b1 = Button(bg_img, image=self.photoimg5,command=self.face_data, cursor="hand2")
  b1.place(x=450, y=90, width=150, height=150)

  b1_2 = Button(bg_img, text="Face Detector",command=self.face_data, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_2.place(x=450, y=240, width=150, height=30)

  
  #Attendance  button
  img6 = Image.open(
      r"college_images\report.jpg")
  img6 = img6.resize((150, 150), Image.ANTIALIAS)
  self.photoimg6 = ImageTk.PhotoImage(img6)
  b1 = Button(bg_img, image=self.photoimg6,command=self.attendance_data, cursor="hand2")
  b1.place(x=650, y=90, width=150, height=150)

  b1_3 = Button(bg_img, text="Attendance",command=self.attendance_data, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_3.place(x=650, y=240, width=150, height=30)
  
  
  #Help desk button
  img7 = Image.open(
      r"college_images\help-desk.jpg")
  img7 = img7.resize((150, 150), Image.ANTIALIAS)
  self.photoimg7 = ImageTk.PhotoImage(img7)
  b1 = Button(bg_img, image=self.photoimg7,command=self.help_data, cursor="hand2")
  b1.place(x=850, y=90, width=150, height=150)

  b1_2 = Button(bg_img, text="Help desk",command=self.help_data, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_2.place(x=850, y=240, width=150, height=30)

  #Train Face button
  img8 = Image.open(
      r"college_images\Train.jpg")
  img8 = img8.resize((150, 150), Image.ANTIALIAS)
  self.photoimg8 = ImageTk.PhotoImage(img8)
  b1 = Button(bg_img, image=self.photoimg8,command=self.train_data, cursor="hand2")
  b1.place(x=250, y=310, width=150, height=150)

  b1_1 = Button(bg_img, text="Train Face",command=self.train_data, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg
  ="darkblue", fg="white")
  b1_1.place(x=250, y=450, width=150, height=30)
  
  
  #photos Face button
  img9 = Image.open(
      r"college_images\photos.jpg")
  img9 = img9.resize((150, 150), Image.ANTIALIAS)
  self.photoimg9 = ImageTk.PhotoImage(img9)
  b1 = Button(bg_img,command=self.open_img, image=self.photoimg9, cursor="hand2")
  b1.place(x=450, y=310, width=150, height=150)

  b1_1 = Button(bg_img,command=self.open_img, text="Photos", cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_1.place(x=450, y=450, width=150, height=30)
  
  
  #developer button
  img10 = Image.open(
      r"college_images\developer.jpg")
  img10 = img10.resize((150, 150), Image.ANTIALIAS)
  self.photoimg10 = ImageTk.PhotoImage(img10)
  b1 = Button(bg_img, image=self.photoimg10,command=self.developer_data, cursor="hand2")
  b1.place(x=650, y=310, width=150, height=150)

  b1_1 = Button(bg_img, text="Developer",command=self.developer_data, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_1.place(x=650, y=450, width=150, height=30)
  
  
  #exit button
  img11 = Image.open(
      r"college_images\exit.jpg")
  img11 = img11.resize((150, 150), Image.ANTIALIAS)
  self.photoimg11 = ImageTk.PhotoImage(img11)
  b1 = Button(bg_img, image=self.photoimg11,command=self.iexit, cursor="hand2")
  b1.place(x=850, y=310, width=150, height=150)

  b1_1 = Button(bg_img, text="Exit",command=self.iexit, cursor="hand2", font=(
      "times new roman", 15, "bold"), bg="darkblue", fg="white")
  b1_1.place(x=850, y=450, width=150, height=30)
  
  
  
  
 #============open image====
 def open_img(self):
     os.startfile("data")
  
  
 def iexit(self):
     self.iexit=tkinter.messagebox.askyesno("Face Recognition","Are you sure exit this project" ,parent=self.root)
     if self.iexit>0:
         self.root.destroy()
     else:
         return
  
  
  
  
  
  
  
  #===============Function  buttion========
  
  
 def student_details(self):
      
     self.new_window=Toplevel(self.root)
     self.app=Student(self.new_window)
     
 def train_data(self):

     self.new_window = Toplevel(self.root)
     self.app = train(self.new_window)
     
 def face_data(self):
 
     self.new_window = Toplevel(self.root)
     self.app = face_recognizer(self.new_window)
 
 def attendance_data(self):
  
     self.new_window = Toplevel(self.root)
     self.app = attendance(self.new_window)
     
 def developer_data(self):

     self.new_window = Toplevel(self.root)
     self.app = developer(self.new_window)
     
     
 def help_data(self):
 
     self.new_window = Toplevel(self.root)
     self.app = help(self.new_window)

      

  
  
  
  
  
if __name__=="__main__":
 root=Tk()
 obj=face_recognization_system(root)
 root.mainloop()