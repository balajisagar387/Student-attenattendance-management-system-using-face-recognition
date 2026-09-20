# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 16:03:23 2022

@author: Birajdar balaji
"""
from distutils.command.config import config
from ast import Lambda
from distutils.command.config import config
from logging import exception
from textwrap import fill
from tkinter import*
from tkinter import ttk
import os

from turtle import width
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from numpy import number
from sqlalchemy import Integer 
from tkcalendar import DateEntry




class Student:
 def __init__(self,roots):
  self.roots=roots
  self.roots.geometry("1550x790+0+0")
  self.roots.title("Student Attendance Management System")
  roots.iconbitmap(r"college_images\icon.ico")
  
  
  
  #==================varibles==================
  
  self.var_dep=StringVar()
  self.var_course=StringVar()
  self.var_year = StringVar()
  self.var_sem = StringVar()
  self.var_id = StringVar()
  self.var_name = StringVar()
  self.var_div = StringVar()
  self.var_roll = StringVar()
  self.var_gender = StringVar()
  self.var_dob = StringVar()
  self.var_email = StringVar()
  self.var_phone = StringVar()
  self.var_add = StringVar()
  self.var_teacher = StringVar()
  self.var_course = StringVar()
  
  
  
  img = Image.open(r"college_images\iStock-182059956_18390_t12.jpg")
  img= img.resize((500,130),Image.ANTIALIAS)
  self.photoimg=ImageTk.PhotoImage(img)
  f_lbl=Label(self.roots,image=self.photoimg)
  f_lbl.place(x=0,y=0,width=423,height=130)
  
  img1 = Image.open(
      r"college_images\face-recognition.png")
  img1 = img1.resize((500, 130), Image.ANTIALIAS)
  self.photoimg1 = ImageTk.PhotoImage(img1)
  f_lbl = Label(self.roots, image=self.photoimg1)
  f_lbl.place(x=423, y=0, width=430, height=130)
  
  img2 = Image.open(
      r"college_images\smart-attendance.jpg")
  img2 = img2.resize((500, 130), Image.ANTIALIAS)
  self.photoimg2 = ImageTk.PhotoImage(img2)
  f_lbl = Label(self.roots, image=self.photoimg2)
  f_lbl.place(x=850, y=0, width=432, height=130)
  
  
  
  
  
  
  
  
   # bg image
  """img3 = Image.open(
      r"college_images\wp2551980.jpg")
  img3 = img3.resize((1280, 750), Image.ANTIALIAS)
  self.photoimg3 = ImageTk.PhotoImage(img3)
  bg_img = Label(self.roots, image=self.photoimg3)
  bg_img.place(x=0, y=130, width=1280, height=530)"""
  bg_img=Frame(self.roots)
  bg_img.place(x=0, y=130, width=1280, height=530)
  
  
  
  #lable title
  
  title_lbl=Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font =("times new roman",25,"bold"),bg="white",fg="darkgreen")
  title_lbl.place(x=0,y=0,width=1280,height=40)
  
  
  #main frame
  main_frame=Frame(bg_img,bd=2)
  main_frame.place(x=15,y=45,width=1220,height=475)
  
  
  #left side label
  Left_Frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
  Left_Frame.place(x=5,y=5,width=600,height=465)
  
  
  
  #current course
  courrent_course_Frame=LabelFrame(Left_Frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",font=("times new roman",12,"bold"))
  courrent_course_Frame.place(x=5,y=5,width=590,height=110)
  
   #department
  dep_lable = Label(courrent_course_Frame, text="Department",
                    font=("times new roman", 12, "bold"),bg="white")
  dep_lable.grid(row=0,column=0,padx=10)
  dep_combo = ttk.Combobox(courrent_course_Frame,textvariable=self.var_dep,
                           font=("times new roman", 12, "bold"), width=17, state='readonly')
  dep_combo['values']=("Select Department","computer","IT","civil","Mechanical")
  dep_combo.current(0)
  dep_combo.grid(row=0,column=1,padx=10,pady=5)
  
  #course
  course_lable = Label(courrent_course_Frame, text="Course",
                    font=("times new roman", 12, "bold"), bg="white")
  course_lable.grid(row=0, column=2, padx=10,sticky=W)
  course_combo = ttk.Combobox(courrent_course_Frame, textvariable=self.var_course,
                           font=("times new roman", 12, "bold"), width=17, state="readonly")
  course_combo['values'] = ("Select Course", "B.TECH","M.TECH",
                         "SE", "BCA", "MCA","BE")
  course_combo.current(0)
  course_combo.grid(row=0, column=3, padx=10, pady=5,sticky=W)
  
  #year
  year_lable = Label(courrent_course_Frame, text="Year",
                    font=("times new roman", 12, "bold"), bg="white")
  year_lable.grid(row=1, column=0, padx=10)
  year_combo = ttk.Combobox(courrent_course_Frame, textvariable=self.var_year,
                           font=("times new roman", 12, "bold"), width=17, state="readonly")
  year_combo['values'] = ("Select Year", "2020-21",
                         "2021-22", "2022-23", "2023-24")
  year_combo.current(0)
  year_combo.grid(row=1, column=1, padx=10, pady=5,sticky=W)
  
  
  #semester
  
  semester_lable = Label(courrent_course_Frame, text="Semester",
                    font=("times new roman", 12, "bold"), bg="white")
  semester_lable.grid(row=1, column=2, padx=10)
  semester_combo = ttk.Combobox(courrent_course_Frame, textvariable=self.var_sem,
                           font=("times new roman", 12, "bold"), width=17, state='readonly')
  semester_combo['values'] = ("Select Semester", "Semester-1",
                         "Semester-2")
  semester_combo.current(0)
  semester_combo.grid(row=1, column=3, padx=10, pady=5
                      ,sticky=W)
  
  
  #class student info
  class_student_Frame = LabelFrame(Left_Frame, bd=2, bg="white", relief=RIDGE,
                                     text="class student Information", font=("times new roman", 12, "bold"))
  class_student_Frame.place(x=5, y=115, width=590, height=440)
  
  #student  id
  studentid_lable = Label(class_student_Frame, text="StudentID",
                         font=("times new roman", 12, "bold"), bg="white")
  studentid_lable.grid(row=0, column=0, padx=10, pady=3, sticky=W)
  
  
  studentid_entry = ttk.Entry(class_student_Frame, textvariable=self.var_id, width=17, font=(
      "times new roman", 12, "bold"))
  
  studentid_entry.grid(row=0, column=1, padx=5, pady=3, sticky=W)
  
  #student  name
  studentname_lable = Label(class_student_Frame, text="Student Name",
                          font=("times new roman", 12, "bold"), bg="white")
  studentname_lable.grid(row=0, column=2, padx=10, pady=3, sticky=W)

  studentname_entry = ttk.Entry(class_student_Frame, textvariable=self.var_name, width=17, font=(
      "times new roman", 12, "bold"))

  studentname_entry.grid(row=0, column=3, padx=5, pady=3, sticky=W)
  
  #student  division
  studentdiv_lable = Label(class_student_Frame, text="Class Division",
                          font=("times new roman", 12, "bold"), bg="white")
  studentdiv_lable.grid(row=1, column=0, padx=10, pady=3, sticky=W)

  
  div_combo = ttk.Combobox(class_student_Frame, textvariable=self.var_div,state='readonly',
                           font=("times new roman", 12, "bold"), width=15)
  div_combo['values'] = ("A", "B","C")
  div_combo.current(0)
  div_combo.grid(row=1, column=1, padx=5, pady=3,sticky=W)
  
  #student  roll no
  studentroll_lable = Label(class_student_Frame, text="Roll No",
                          font=("times new roman", 12, "bold"), bg="white")
  studentroll_lable.grid(row=1, column=2, padx=10, pady=3, sticky=W)
  

  studentroll_entry = ttk.Entry(class_student_Frame, textvariable=self.var_roll, width=17, font=(
      "times new roman", 12, "bold"))

  studentroll_entry.grid(row=1, column=3, padx=5, pady=3, sticky=W)
  
  
  #student  gender
  studentgender_lable = Label(class_student_Frame, text="Gender:",
                          font=("times new roman", 12, "bold"), bg="white")
  studentgender_lable.grid(row=2, column=0, padx=10, pady=3, sticky=W)

  
  gender_combo = ttk.Combobox(class_student_Frame, textvariable=self.var_gender,state='readonly',
                           font=("times new roman", 12, "bold"), width=15,)
  gender_combo['values'] = ("Male", "Female","Other")
  gender_combo.current(0)
  gender_combo.grid(row=2, column=1, padx=5, pady=3,sticky=W)
  
  
  
  #student  DOB
  studentbob_lable = Label(class_student_Frame, text="DOB",
                           font=("times new roman", 12, "bold"), bg="white")
  studentbob_lable.grid(row=2, column=2, padx=10, pady=3, sticky=W)

  studentbob_entry = DateEntry(class_student_Frame, selectmode='day', year=2000, month=6,day=1,  state='readonly',
                               font=("times new roman", 12, "bold"), width=15 , textvariable=self.var_dob)

  studentbob_entry.grid(row=2, column=3, padx=5, pady=3, sticky=W)
  
  
  
  
  
  
  
  
  
  
  #student  Email
  studentemail_lable = Label(class_student_Frame, text="Email",
                          font=("times new roman", 12, "bold"), bg="white")
  studentemail_lable.grid(row=3, column=0, padx=10, pady=3, sticky=W)

  studentemail_entry = ttk.Entry(class_student_Frame,textvariable=self.var_email, width=17, font=(
      "times new roman", 12, "bold"))

  studentemail_entry.grid(row=3, column=1, padx=5, pady=3, sticky=W)
  
  #student  phone no
  studentphone_lable = Label(class_student_Frame, text="Phone No",
                          font=("times new roman", 12, "bold"), bg="white")
  studentphone_lable.grid(row=3, column=2, padx=10, pady=3, sticky=W)

  studentphone_entry = ttk.Entry(class_student_Frame, textvariable=self.var_phone, width=17, font=(
      "times new roman", 12, "bold"))

  studentphone_entry.grid(row=3, column=3, padx=5, pady=3, sticky=W)
  
  #student  address
  studentadd_lable = Label(class_student_Frame, text="Address",
                          font=("times new roman", 12, "bold"), bg="white")
  studentadd_lable.grid(row=4, column=0, padx=10, pady=3, sticky=W)

  studentadd_entry = ttk.Entry(class_student_Frame, textvariable=self.var_add, width=17, font=(
      "times new roman", 12, "bold"))

  studentadd_entry.grid(row=4, column=1, padx=5, pady=3, sticky=W)
  
  #teacher name
  studenttech_lable = Label(class_student_Frame, text="Teacher Name",
                          font=("times new roman", 12, "bold"), bg="white")
  studenttech_lable.grid(row=4, column=2, padx=10, pady=3, sticky=W)

  studenttech_entry = ttk.Entry(class_student_Frame, textvariable=self.var_teacher, width=17, font=(
      "times new roman", 12, "bold"))

  studenttech_entry.grid(row=4, column=3,padx=5, pady=3, sticky=W)
  
  #===========radiobutton
  self.var_radio1=StringVar()
  radiobtn1 = ttk.Radiobutton(
      class_student_Frame, variable=self.var_radio1, text="take photo sample", value="Yes")
  radiobtn1.grid(row=6,column=0)
  

  radiobtn2 = ttk.Radiobutton(
      class_student_Frame, variable=self.var_radio1, text="No photo sample", value="No")
  radiobtn2.grid(row=6, column=2)
  
  
  #button frame
  btn_frame=Frame(class_student_Frame,bd=2,relief=RIDGE,bg="white" )
  btn_frame.place(x=0,y=190,width=590,height=40 )
  
  save_btn = Button(btn_frame, text="Save",command=self.add_data, font=("times new roman", 12, "bold"),bg="blue",width=15,  fg="white")
  save_btn.grid(row=0,column=0)
  
  update_btn = Button(btn_frame, text="Update",command=self.update ,font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  update_btn.grid(row=0, column=1)
  
  delete_btn = Button(btn_frame, text="Delete",command=self.delete_data, font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  delete_btn.grid(row=0, column=2)
  
  reset_btn = Button(btn_frame, text="Reset", font=(
      "times new roman", 12, "bold"),command=self.reset_data, bg="blue", width=17,  fg="white")
  reset_btn.grid(row=0, column=3)
  
  btn_frame1 = Frame(class_student_Frame, bd=2, relief=RIDGE, bg="white")
  btn_frame1.place(x=0, y=240, width=590, height=35)

  update_photo_btn = Button(btn_frame1,command=self.genarate_dataset, text="Update Photo Sample", font=(
      "times new roman", 12, "bold"), bg="blue", width=30,  fg="white")
  update_photo_btn.grid(row=0, column=0)
  
  """update_photo_btn = Button(btn_frame1, text="Update Photo Sample", font=(
      "times new roman", 12, "bold"), bg="blue", width=35,  fg="white")
  update_photo_btn.grid(row=0, column=1)
  """
  
  
  
  
  
  #right side label==============================================!!!!!!!!!!!!!!!!!!
  
  Right_Frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
  Right_Frame.place(x=615,y=5,width=600,height=470)
  
  img_right = Image.open( r"college_images\AdobeStock_303989091.jpeg")
  img_right = img_right.resize((600, 110), Image.ANTIALIAS)
  self.photoimg_right = ImageTk.PhotoImage(img_right)
  f_lbl = Label(Right_Frame, image=self.photoimg_right)
  f_lbl.place(x=5, y=0, width=590, height=110)
  
  
  
  #===============searching system========
  
  search_Frame = LabelFrame(Right_Frame, bd=2, bg="white", relief=RIDGE,
                                   text="Search System", font=("times new roman", 12, "bold"))
  search_Frame.place(x=5, y=115, width=590, height=60)
  
  search_lable = Label(search_Frame, text="Search By:",
                             font=("times new roman", 12, "bold"), bg="red",width=12,fg="white")
  search_lable.grid(row=0, column=0, padx=1, pady=3, sticky=W)
  
  #search==========
  self.var_drop=StringVar()
  
  drop = ttk.Combobox(search_Frame,textvariable=self.var_drop,
                                font=("times new roman", 12, "bold"), width=12, state='readonly')
  drop['values'] = ("Select ", "Student_id","Roll","Name",
                              "Phone")
  drop.current(0)
  drop.grid(row=0, column=1, padx=1, pady=3, sticky=W)
  
  
  
  self.var_search=StringVar()
  search_entry = ttk.Entry(search_Frame,textvariable=self.var_search, width=12, font=(
      "times new roman", 12, "bold"))
  search_entry.grid(row=0, column=2, padx=3, pady=3, sticky=W)
  
  search_btn = Button(search_Frame,command=self.search_now, text="Search", font=(
      "times new roman", 12, "bold"), bg="blue", width=12,  fg="white")
  search_btn.grid(row=0, column=3,padx=3)
  
  showall_btn = Button(search_Frame,command=self.fetch_data, text="Show All", font=(
      "times new roman", 12, "bold"), bg="blue", width=12,  fg="white")
  showall_btn.grid(row=0, column=4)
  #===========table frame
  table_Frame = LabelFrame(Right_Frame, bd=2, bg="white", relief=RIDGE)
  table_Frame.place(x=5, y=170, width=590, height=270)
  
  
  scroll_x=ttk.Scrollbar(table_Frame,orient=HORIZONTAL)
  scroll_y = ttk.Scrollbar(table_Frame, orient=VERTICAL)

  self.student_table = ttk.Treeview(table_Frame, column=("dep", "course", "year", "sem", "id", "name" , "div", "roll",
                                    "gender","dob","email", "phone",  "address", "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
  scroll_x.pack(side=BOTTOM,fill=X)
  scroll_y.pack(side=RIGHT, fill=Y)
  
  scroll_x.config(command=self.student_table.xview)
  scroll_y.config(command=self.student_table.yview)
  
  self.student_table.heading("dep",text="Department")
  self.student_table.heading("course", text="Course")
  self.student_table.heading("year", text="Year")
  self.student_table.heading("sem", text="Semester")
  self.student_table.heading("id", text="StudentID")
  self.student_table.heading("name", text="Student Name")
  self.student_table.heading("div", text="Class Division")
  self.student_table.heading("roll", text="Roll No")
  self.student_table.heading("gender", text="Gender")
  self.student_table.heading("dob", text="DOB")
  self.student_table.heading("email", text="Email")
  self.student_table.heading("phone", text="Phone No")
  self.student_table.heading("address", text="Address")
  self.student_table.heading("teacher", text="Teacher Name")
  self.student_table.heading("photo", text="Photo Sample")
  
  self.student_table["show"]="headings"
  
  
  self.student_table.column("dep", width=100)
  self.student_table.column("course", width=100)
  self.student_table.column("year", width=100)
  self.student_table.column("sem", width=100)
  self.student_table.column("id", width=100)
  self.student_table.column("name", width=100)
  self.student_table.column("div", width=100)
  self.student_table.column("roll", width=100)
  self.student_table.column("gender", width=100)
  self.student_table.column("dob", width=100)
  self.student_table.column("email", width=100)
  self.student_table.column("phone", width=100)
  self.student_table.column("address", width=100)
  self.student_table.column("teacher", width=100)
  self.student_table.column("photo", width=100)
  
  
  
  
  
  self.student_table.pack(fill=BOTH,expand=1)
  self.student_table.bind("<ButtonRelease>",self.get_cursor)
  self.fetch_data()
  
  
  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)
  
  
 #validate all fields

#validate name



 def search_now(self):
     if self.var_drop.get() == "" or self.var_search.get() == "":
         messagebox.showerror("Error","Please select option",parent=self.roots)
         
     
     else:
         try:
             conn = mysql.connector.connect(
                 host="localhost", user="root", password="balu123", database="student_management")

             my_cursor = conn.cursor()
             my_cursor.execute("select * from student where "+str(self.var_drop.get())+" LIKE '%"+str(self.var_search.get())+"%'")
             rows=my_cursor.fetchall()
             
             if len(rows)!=0:
                 self.student_table.delete(*self.student_table.get_children())
                 for i in rows:
                     self.student_table.insert("",END,values=i)
                 conn.commit()

             conn.close()
             
         except Exception as es:
             messagebox.showerror(
                 "Error", f"Due To :{str(es)}", parent=self.roots)

             
     



#back button
 def backtoMain(self):

     self.roots.destroy()
  #===================function declaretion===========

 def add_data(self):
     
     
     
     special_ch = ['@', '.']
     msg = ''
     phone = self.var_phone.get()
     email=self.var_email.get()
     name_str = self.var_name.get()
     id=self.var_id.get()
     roll=self.var_roll.get()
     teacher=self.var_teacher.get()
     
     if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "" or self.var_roll.get() == "" or self.var_dob.get() == "" or self.var_email.get() == "" or self.var_radio1.get() == "" or self.var_phone.get() == "" or self.var_course.get() == "Select Course" or self.var_sem.get() == "Select Semester" or self.var_add.get() == "" or self.var_year.get() == "Select Year":
         messagebox.showerror(
             "Error", "All Field are Required", parent=self.roots)
     elif not any(ch.isdigit() for ch in id) or any(ch.isalpha() for ch in id):
         msg = 'Enter valid id'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     elif any(ch.isdigit() for ch in name_str):
         msg = 'Name cannot have numbers'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
         
     elif not any(ch.isdigit() for ch in roll) or any(ch.isalpha() for ch in roll):
         msg = 'Enter valid Roll number'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     
     
     elif not any( ch in special_ch for ch in email):
                    msg = 'invalid email!'
                    messagebox.showerror(
                        "Error", msg, parent=self.roots)
     
     elif not any(ch.isdigit() for ch in phone) or len(phone) != 10 or any(ch.isalpha() for ch in phone):
         msg = 'Enter valid number'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
         
     elif any(ch.isdigit() for ch in teacher):
         msg = 'Enter valid Teacher name'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     
     else :
         
         try:
             
             conn = mysql.connector.connect(
                 host="localhost", user="root", password="balu123", database="student_management")

             my_cursor = conn.cursor()
             my_cursor.execute(
                 "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                 (
                  self.var_dep.get(),
                  self.var_course.get(),
                  self.var_year.get(),
                  self.var_sem.get(),
                  self.var_id.get(),
                  self.var_name.get(),
                  self.var_div.get(),
                  self.var_roll.get(),
                  self.var_gender.get(),
                  self.var_dob.get(),
                  self.var_email.get(),
                  self.var_phone.get(),
                  self.var_add.get(),
                  self.var_teacher.get(),
                  self.var_radio1.get()
                  ))
             conn.commit()
             self.fetch_data()
             #validate
             
             
             conn.close()
             if self.var_radio1.get() == "Yes" :
                 self.genarate_dataset()
             messagebox.showinfo(
                 "success", "Student details has been added successfully", parent=self.roots)

         except Exception as es:
             messagebox.showerror(
                 "Error", f"Due To :{str(es)}", parent=self.roots)
         

         
         
             
             
 def fetch_data(self):
     conn = mysql.connector.connect(
         host="localhost", user="root", password="balu123", database="student_management")

     my_cursor = conn.cursor()
     my_cursor.execute("select * from student")
     data=my_cursor.fetchall()
     
     if len(data)!=0:
         self.student_table.delete(*self.student_table.get_children())
         for i in data :
             self.student_table.insert("", END, values=i)
         conn.commit()
     conn.close()
        
        
# ===================get curson===========
 def get_cursor(self,event=""):
     cursor_focus=self.student_table.focus()
     content=self.student_table.item(cursor_focus)
     data=content["values"]
     
     self.var_dep.set(data[0]),
     self.var_course.set(data[1]),
     self.var_year.set(data[2]),
     self.var_sem.set(data[3]),
     self.var_id.set(data[4]),
     self.var_name.set(data[5]),
     self.var_div.set(data[6]),
     self.var_roll.set(data[7]),
     self.var_gender.set(data[8]),
     self.var_dob.set(data[9]),
     self.var_email.set(data[10]),
     self.var_phone.set(data[11]),
     self.var_add.set(data[12]),
     self.var_teacher.set(data[13]),
     self.var_radio1.set(data[14]),
      
     
        
#=========================Update  Function============


 def update(self):
     special_ch = ['@', '.']
     msg = ''
     phone = self.var_phone.get()
     email = self.var_email.get()
     name_str = self.var_name.get()
     id = self.var_id.get()
     roll = self.var_roll.get()
     teacher = self.var_teacher.get()
     if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "" or self.var_course.get() == "Select Course" or self.var_sem.get() == "Select Semester" or self.var_year.get() == "Select Year":
         messagebox.showerror("Error","All Field are Required",parent=self.roots)
         
     elif not any(ch.isdigit() for ch in id) or any(ch.isalpha() for ch in id):
         msg = 'Please Enter valid id'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     elif any(ch.isdigit() for ch in name_str):
         msg = 'Name cannot have numbers'
         messagebox.showerror(
             "Error", msg, parent=self.roots)

     elif not any(ch.isdigit() for ch in roll) or any(ch.isalpha() for ch in roll):
         msg = 'Please Enter valid Roll number'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     elif not any(ch in special_ch for ch in email):
         msg = 'Please Enter valid email!'
         messagebox.showerror(
             "Error", msg, parent=self.roots)

     elif not any(ch.isdigit() for ch in phone) or len(phone) != 10 or any(ch.isalpha() for ch in phone):
         msg = 'Please Enter valid number'
         messagebox.showerror(
             "Error", msg, parent=self.roots)

     elif any(ch.isdigit() for ch in teacher):
         msg = 'Please Enter valid Teacher name'
         messagebox.showerror(
             "Error", msg, parent=self.roots)
     
     else:
         try:
             
             Update=messagebox.askyesno("update","do you want to update this student details" ,parent=self.roots)
             if Update>0:
                 conn = mysql.connector.connect(
                     host="localhost", user="root", password="balu123", database="student_management")

                 my_cursor = conn.cursor()
                 
                 my_cursor.execute("update student set Dep=%s,Course=%s,Year=%s,Semester=%s,Name=%s,Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,Teacher=%s,PhotoSample=%s where Student_id=%s",(
                                   self.var_dep.get(),
                                   self.var_course.get(),
                                   self.var_year.get(),
                                   self.var_sem.get(),
                                   self.var_name.get(),
                                   self.var_div.get(),
                                   self.var_roll.get(),
                                   self.var_gender.get(),
                                   self.var_dob.get(),
                                   self.var_email.get(),
                                   self.var_phone.get(),
                                   self.var_add.get(),
                                   self.var_teacher.get(),
                                   self.var_radio1.get(),
                                   self.var_id.get()
                                   ))
             
             else:
                 if not Update :
                     
                     return
             messagebox.showinfo("success","Student details successfully update completed",parent=self.roots)
             conn.commit()
             self.fetch_data()
             self.reset_data()
             conn.close()
         except Exception as es:
             messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.roots)
             
             
             
#=============          delete function ===========
 def delete_data(self):
     if self.var_id.get()=="":
         messagebox.showerror("Error","Student id must be required",parent=self.roots)
         
     else:
         try:
             delete=messagebox.askyesno("Delete Student Page" ,"Do you want to delete this student record",parent =self.roots)
             if delete>0:
                 
                 conn = mysql.connector.connect(
                     host="localhost", user="root", password="balu123", database="student_management")

                 my_cursor = conn.cursor()
                 
                 sql="delete from student where Student_id=%s"
                 val=(self.var_id.get(),)
                 my_cursor.execute(sql,val)
                 
                 
                 id = self.var_id.get()

                 

                 target = "data"
                 for file in os.listdir(target):
                     file_name = "data\\"+str(file)
                     if file.startswith("user."+str(id)):
                         os.remove(file_name)
                         
                 
                 
             else:
                 if not delete:
                     return
                 
             
             conn.commit()
             self.fetch_data()
             self.reset_data()
             conn.close()
             messagebox.showinfo("Delete","Successfully Deleted student Record",parent=self.roots)
         except EXCEPTION as es:
            messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.roots)
            
            
            
#=========reset

 def reset_data(self):
     self.var_dep.set("Select Department")
     self.var_course.set("Select Course")
     self.var_year.set("Select Year")
     self.var_sem.set("Select Semester")
     self.var_id.set("")
     self.var_name.set("")
     self.var_div.set("Select Division")
     self.var_roll.set("")
     self.var_gender.set("")
     self.var_dob.set("")
     self.var_email.set("")
     self.var_phone.set("")
     self.var_add.set("")
     self.var_teacher.set("")
     self.var_radio1.set("")
     
#=============== Genarate data set  take photo sample===========
 def genarate_dataset(self):
     if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_radio1.get() == "No" or self.var_id.get() == "":
         messagebox.showerror(
             "Error", "All Field are Required", parent=self.roots)

     else:
         try:
             

             
             conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123",database="student_management")

             my_cursor = conn.cursor()

             
             
             my_cursor.execute("update student set Dep=%s,Course=%s,Year=%s,Semester=%s,Name=%s,Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,Teacher=%s,PhotoSample=%s where Student_id=%s", (
                 self.var_dep.get(),
                 self.var_course.get(),
                 self.var_year.get(),
                 self.var_sem.get(),
                 self.var_name.get(),
                 self.var_div.get(),
                 self.var_roll.get(),
                 self.var_gender.get(),
                 self.var_dob.get(),
                 self.var_email.get(),
                 self.var_phone.get(),
                 self.var_add.get(),
                 self.var_teacher.get(),
                 self.var_radio1.get(),
                 self.var_id.get()
             ))
             my_cursor.execute("select Student_id from student")
             myresult = my_cursor.fetchall()

             
             id=self.var_id.get()

             #=================== load predifiend data on face frontals from opencv====
             
             face_classifier=cv2.CascadeClassifier("face_classifier.xml")

             def face_cropped(img):
                 gray=cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
                 faces=face_classifier.detectMultiScale(gray,1.3,5)
                 
                 for (x,h,w,y) in faces:
                     face_cropped=img[y:y+h,x:x+w]
                     return face_cropped
                 
                 
             cap=cv2.VideoCapture(0)
             img_id=0
             while True:
                 ret,my_frame=cap.read()
                 if face_cropped(my_frame) is not None:
                     img_id+=1
                     
                     face=cv2.resize(face_cropped(my_frame),(500,500))
                     
                     face=cv2.cvtColor(face,cv2.COLOR_BGRA2GRAY)
                     file_name = r"data\user."+str(id)+"."+str(img_id)+".jpg"
                     cv2.imwrite(file_name,face)
                     cv2.putText(face,str(img_id),(30,30),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                     cv2.imshow("Crooped Face", face)
                 if cv2.waitKey(1)==13 or int(img_id)==150:
                     break
             cap.release()
             conn.commit()
             self.fetch_data()
             self.reset_data()
             conn.close()
             cv2.destroyAllWindows()
             #messagebox.showinfo("Result","Genarating data sets complete!!!!")
         except Exception as es:
            messagebox.showerror(
                "Error", f"Due To : {str(es)}", parent=self.roots)
            print(es)




                 
                 
                 

     
  
  
  
  
  
  
  
  
 
     
  
  
  
if __name__=="__main__":
    roots=Tk()
    obj=Student(roots)
    roots.mainloop()
   