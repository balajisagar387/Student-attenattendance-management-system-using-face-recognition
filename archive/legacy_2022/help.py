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


class help:
 def __init__(self, root):
  self.root = root
  self.root.geometry("1550x790+0+0")
  self.root.title("Face Recognization System")

  title_lbl = Label(self.root, text="HELP DESK", font=(
      "times new roman", 25, "bold"), bg="white", fg="blue")
  title_lbl.place(x=0, y=0, width=1280, height=40)

  img_top = Image.open(
      r"college_images\1_5TRuG7tG0KrZJXKoFtHlSg.jpeg")
  img_top = img_top.resize((1275, 600), Image.ANTIALIAS)
  self.photoimgtop = ImageTk.PhotoImage(img_top)
  f_lb2 = Label(self.root, image=self.photoimgtop)
  f_lb2.place(x=0, y=40, width=1275, height=600)


  dev_lable = Label(f_lb2, text="Email:balajisagar387@gmail.com",
                  font=("times new roman", 17, "bold"), fg="blue", bg="white")
  dev_lable.place(x=450, y=200)
  
  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)

 def backtoMain(self):

     self.root.destroy()
  
  
  
if __name__ == "__main__":
    root = Tk()
    obj = help(root)
    root.mainloop()
