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


class developer:
 def __init__(self, root):
  self.root = root
  self.root.geometry("1550x790+0+0")
  self.root.title("Student Attendance Management System")
  
  title_lbl = Label(self.root, text="DEVELOPER", font=(
      "times new roman", 25, "bold"), bg="white", fg="blue")
  title_lbl.place(x=0, y=0, width=1280, height=40)

  img_top = Image.open(
      r"college_images\dev.jpg")
  img_top = img_top.resize((1275, 600), Image.ANTIALIAS)
  self.photoimgtop = ImageTk.PhotoImage(img_top)
  f_lbl = Label(self.root, image=self.photoimgtop)
  f_lbl.place(x=0, y=40, width=1275, height=600)
  
  #===========frame
  main_frame = Frame(f_lbl, bd=2, relief=RIDGE, bg="white")
  main_frame.place(x=800, y=0, width=600, height=450)
  
  """img_top1 = Image.open(
      r"college_images\tony.jpg")
  img_top1 = img_top1.resize((200, 180), Image.ANTIALIAS)
  self.photoimgtop1 = ImageTk.PhotoImage(img_top1)
  f_lb2 = Label(main_frame, image=self.photoimgtop1)
  f_lb2.place(x=270, y=0, width=200, height=180)"""
  
  
  #============developer 
  dev_lable = Label(main_frame, text="Hello There.",
                           font=("times new roman", 17, "bold"),fg="blue", bg="white")
  dev_lable.place(x=0,y=0)
  #1)Balaji  birajdar .\n" "2)Aradhya Telkhade.\n3)Abhishek Patil
  dev_lable = Label(main_frame, text="We are The Team of 3  developer.",
                    font=("times new roman", 17, "bold"), fg="blue", bg="white")
  dev_lable.place(x=0, y=30)
  dev_lable = Label(main_frame, text="Who develope this app.",
                    font=("times new roman", 17, "bold"), fg="blue", bg="white")
  dev_lable.place(x=0, y=60)
  
  
  
  img_topleft = Image.open(
      r"college_images\KPIs-and-Agile-software-development-metrics-for-teams-1.jpg")
  img_topleft = img_topleft.resize((465, 300), Image.ANTIALIAS)
  self.photoimgtopleftimg_topleft = ImageTk.PhotoImage(img_topleft)
  f_lb3 = Label(main_frame, image=self.photoimgtopleftimg_topleft)
  f_lb3.place(x=0, y=180, width=465, height=300)

  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)
 def backtoMain(self):
 
     self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = developer(root)
    root.mainloop()
