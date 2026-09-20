from distutils.command.config import config
from ast import Lambda
from distutils.command.config import config
from logging import exception
from optparse import Values
from textwrap import fill
from tkinter import*
import os
import csv
from tkinter import filedialog
from tkinter import ttk
from turtle import width
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from numpy import integer, row_stack
import re 

mydata=[]
class attendance:
 def __init__(self, root):
  self.root = root
  self.root.geometry("1550x790+0+0")
  self.root.title("ATTENDANCE MANAGEMENT SYSTEM")
  
  
  
  
  
  #=======text variables
  self.var_atten_id=StringVar()
  self.var_atten_roll = StringVar()
  self.var_atten_name = StringVar()
  self.var_atten_dep = StringVar()
  self.var_atten_time = StringVar()
  self.var_atten_date = StringVar()
  self.var_atten_attendance = StringVar()
  
  
  
  
  
  img = Image.open(
      r"college_images\smart-attendance.jpg")
  img = img.resize((670, 200), Image.ANTIALIAS)
  self.photoimg = ImageTk.PhotoImage(img)
  f_lbl = Label(self.root, image=self.photoimg)
  f_lbl.place(x=0, y=0, width=670, height=200)

  img1 = Image.open(
      r"college_images\sample.jpg")
  img1 = img1.resize((670, 200), Image.ANTIALIAS)
  self.photoimg1 = ImageTk.PhotoImage(img1)
  f_lbl = Label(self.root, image=self.photoimg1)
  f_lbl.place(x=670, y=0, width=670, height=200)
  
  
  img3 = Image.open(
      r"college_images\wp2551980.jpg")
  img3 = img3.resize((1280, 750), Image.ANTIALIAS)
  self.photoimg3 = ImageTk.PhotoImage(img3)
  bg_img = Label(self.root, image=self.photoimg3)
  bg_img.place(x=0, y=130, width=1280, height=530)
  
  title_lbl = Label(bg_img, text="ATTENDANCE MANAGEMENT SYSTEM", font=("times new roman", 25, "bold"), bg="white", fg="darkgreen")
  title_lbl.place(x=0, y=0, width=1280, height=40)
  
  #main frame
  main_frame = Frame(bg_img, bd=2)
  main_frame.place(x=15, y=45, width=1220, height=475)

  #left side label
  Left_Frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                          text="Student Attendance Details", font=("times new roman", 12, "bold"))
  Left_Frame.place(x=5, y=5, width=600, height=465)
  
  left_inside_frame = Frame(Left_Frame, bd=2, bg="white", relief=RIDGE)
  left_inside_frame.place(x=0, y=20, width=590, height=400)
  
  
  #================== labled entry
  attendanceid_lable = Label(left_inside_frame, text="AttendanceID",
                          font=("times new roman", 12, "bold"), bg="white")
  attendanceid_lable.grid(row=0, column=0, padx=10, pady=10, sticky=W)

  attendanceid_entry = ttk.Entry(left_inside_frame,textvariable=self.var_atten_id, width=15, font=(
      "times new roman", 12, "bold"))

  attendanceid_entry.grid(row=0, column=1,padx=5,  pady=10, sticky=W)
  #bind and validate
  validate_id = self.root.register(self.checkid)
  attendanceid_entry.config(
      validate='key', validatecommand=(validate_id, '%P'))
  
  #student  roll no
  studentroll_lable = Label(left_inside_frame, text="Roll No",
                            font=("times new roman", 12, "bold"), bg="white")
  studentroll_lable.grid(row=0, column=2, padx=10, pady=10, sticky=W)

  studentroll_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_roll,  width=15, font=(
      "times new roman", 12, "bold"))

  studentroll_entry.grid(row=0, column=3, padx=5, pady=10, sticky=W)
  
  #bind and validate
  validate_roll = self.root.register(self.checkroll)
  studentroll_entry.config(
      validate='key', validatecommand=(validate_roll, '%P'))
  
  #========================name 
  studentbob_lable = Label(left_inside_frame, text="Name",
                           font=("times new roman", 12, "bold"), bg="white")
  studentbob_lable.grid(row=1, column=0, padx=10, pady=10, sticky=W)

  studentbob_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_name,  width=15, font=(
      "times new roman", 12, "bold"))

  studentbob_entry.grid(row=1, column=1, padx=5, pady=10, sticky=W)
  
  #bind and validate
  """validate_name=self.root.register(self.checkname)
  studentbob_entry.config(validate='key',validatecommand=(validate_name,'%P'))"""
  
  
  
  #================department
  dep_lable = Label(left_inside_frame, text="Department",
                    font=("times new roman", 12, "bold"), bg="white")
  dep_lable.grid(row=1, column=2,pady=10, padx=10)
  self.dep_combo = ttk.Combobox(left_inside_frame, textvariable=self.var_atten_dep,
                                   font=("times new roman", 12, "bold"), width=13, state='readonly')
  self.dep_combo["values"] = (
      "Select Department", "computer", "IT", "civil", "Mechanical")
  self.dep_combo.grid(row=1, column=3, padx=5, pady=10)
  self.dep_combo.current(0)
  
  #================time
  time_lable = Label(left_inside_frame, text="Time",
                             font=("times new roman", 12, "bold"), bg="white")
  time_lable.grid(row=2, column=0, padx=10, pady=10, sticky=W)

  time_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_time, width=15, font=(
      "times new roman", 12, "bold"))

  time_entry.grid(row=2, column=1, padx=5, pady=10, sticky=W)
  
  #bind and validate
  """validate_time = self.root.register(self.checktime)
  time_entry.config(
      validate='key', validatecommand=(validate_time, '%P'))"""
  
  #================Date
  date_lable = Label(left_inside_frame, text="Date",
                     font=("times new roman", 12, "bold"), bg="white")
  date_lable.grid(row=2, column=2, padx=10, pady=10, sticky=W)

  date_entry = ttk.Entry(left_inside_frame, textvariable=self.var_atten_date, width=15, font=(
      "times new roman", 12, "bold"))

  date_entry.grid(row=2, column=3, padx=5, pady=10, sticky=W)
  
  #bind and validate
  """validate_date = self.root.register(self.checkdate)
  date_entry.config(
      validate='key', validatecommand=(validate_date, '%P'))"""
  
  #================attendance
  attendance_lable = Label(left_inside_frame, text="Attendance Status",
                    font=("times new roman", 12, "bold"), bg="white")
  attendance_lable.grid(row=3, column=0,pady=10, padx=10)
  self.atten_status = ttk.Combobox(left_inside_frame, textvariable=self.var_atten_attendance,
                        font=("times new roman", 12, "bold"), width=13, state='readonly')
  self.atten_status["values"]=("Status","Present","Absent")
  
  self.atten_status.grid(row=3, column=1, padx=5, pady=10)
  self.atten_status.current(0)

  #button frame
  btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
  btn_frame.place(x=0, y=280, width=590, height=80)

  """importcsv_btn = Button(btn_frame, text="Import csv",command=self.importcsv,  font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  importcsv_btn.grid(row=0, column=0)"""
  
  delete_btn = Button(btn_frame, text="Delete", command=self.delete,  font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  delete_btn.grid(row=0, column=3,pady=10)

  exportcsv_btn = Button(btn_frame, text="Export csv",command=self.exportcsv,  font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  exportcsv_btn.grid(row=0, column=0)

  update_btn = Button(btn_frame, text="update",command=self.update,  font=(
      "times new roman", 12, "bold"), bg="blue", width=15,  fg="white")
  update_btn.grid(row=0, column=1)
  
  reset_btn = Button(btn_frame, text="Reset",command=self.reset_data, font=(
      "times new roman", 12, "bold"),  bg="blue", width=17,  fg="white")
  reset_btn.grid(row=0, column=2)

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  #===============Right side Frame
  right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                           text="Attendance Details", font=("times new roman", 12, "bold"))
  right_frame.place(x=615, y=5, width=600, height=470)
  
  table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
  table_frame.place(x=5, y=5, width=580, height=400)
  
  #================== scrollbar table
  scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
  scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

  self.AttendanceReportTable=ttk.Treeview(table_frame,columns=("id","roll","name","department","time","date","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
  
  
  scroll_x.pack(side=BOTTOM,fill=X)
  scroll_y.pack(side=RIGHT, fill=Y)
  
  scroll_x.config(command=self.AttendanceReportTable.xview)
  scroll_y.config(command=self.AttendanceReportTable.yview)
  
  
  self.AttendanceReportTable.heading("id",text="AttendanceID")
  self.AttendanceReportTable.heading("roll", text="Roll")
  self.AttendanceReportTable.heading("name", text="Name")
  self.AttendanceReportTable.heading("department", text="Department")
  self.AttendanceReportTable.heading("time", text="Time")
  self.AttendanceReportTable.heading("date", text="Date")
  self.AttendanceReportTable.heading("attendance", text="Attendance")
  
  
  self.AttendanceReportTable["show"]="headings"
  
  self.AttendanceReportTable.column("id",width=100)
  self.AttendanceReportTable.column("roll", width=100)
  self.AttendanceReportTable.column("name", width=100)
  self.AttendanceReportTable.column("department", width=100)
  self.AttendanceReportTable.column("time", width=100)
  self.AttendanceReportTable.column("date", width=100)
  self.AttendanceReportTable.column("attendance", width=100)
  
  
  self.AttendanceReportTable.pack(fill=BOTH,expand=1)
  self.fetch_database_data()
  self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)
  
  
  
  
  #==================FETCH DATA
  
  back_lbl = Button(title_lbl, command=self.backtoMain, text="Back", font=(
      "times new roman", 20, ), bg="white", fg="red")
  back_lbl.place(x=1100, y=0, width=100, height=40)




#validation

 def checkid(self, contact):
     
     if contact.isdigit():
         return True
     if len(str(contact)) == 0:
         return True
     else:
         messagebox.showerror(
             "Invalid", "Only numbers allowed in Attendabce id", parent=self.root)
         return False
 """def checkname(self,name):
     if name.isalnum():
         return True
     if len(int(name))==0:
         return True
     
     if name=='':
         return True
     
     else:
         messagebox.showerror('Invalid','Enter Valid Allowed')
         return False"""
     
     
 def checkroll(self,contact):
     if contact.isdigit():
         return True
     if len(str(contact))==0  :
         return True
     else:
         messagebox.showerror(
             "Invalid", "Enter Number only", parent=self.root)
         return False
     
 
         
         
 
         
 """def checktime(self, contact):
     
     if contact.isdigit()or contact==':':
         return True
     elif len(str(contact)) == 0:
         return True
     #elif  contact ==':':
         #return True
     
     
     else:
         messagebox.showerror("Invalid", "Invalid Entry")
         return False"""
     
 """def checkdate(self, contact):
     date = ['/' ]
     if contact.isdigit():
         return True
     if len(str(contact)) == 0:
         return True
     
     else:
         messagebox.showerror("Invalid", "Invalid Date,Enter in the format of 18/3/2000")
         return False"""
     
     



 def backtoMain(self):

     self.root.destroy()
  
 def fetchdata(self,rows):
     self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
     
     for i in rows:
         self.AttendanceReportTable.insert("",END,values=i)
         
 def importcsv(self):
     global mydata
     mydata.clear()
     fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("ALL File","*.*")),parent=self.root)
     
     conn = mysql.connector.connect(
         host="localhost", user="root", password="balu123", database="student_management")

     my_cursor = conn.cursor()
     
     with open(fln) as myfile:
         csvread=csv.reader(myfile,delimiter=",")
         
         for i in csvread:
             mydata.append(i)
         self.fetchdata(mydata)
         
         sql = "insert into attendance(AttendanceID,Roll,Name,Department,Time,Date,Attendance) values(%s,%s,%s,%s,%s,%s,%s)"
         
         my_cursor.execute(sql,mydata)
         conn.commit()
         
         
#===============EXPORT CSV
 def exportcsv(self):
     
     try:
         
         conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123", database="student_management")

         my_cursor = conn.cursor()
         my_cursor.execute("select * from attendance")
         row = my_cursor.fetchall()
         if len(mydata) < 1 and len(row) < 1:
             messagebox.showerror(
                 "No Data", "No Data found to export", parent=self.root)
             return False
         fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(
             ("CSV File", "*.csv"), ("ALL Files", "*.*")), parent=self.root)
         with open(fln, mode="w", newline="") as myfile:
             exp_write = csv.writer(myfile, delimiter=",")
             for i in mydata:
                 exp_write.writerow(i)
                 
             for i in row:
                 exp_write.writerow(i)
             messagebox.showinfo(
                 "Data Export", "Your data exported successfully",parent=self.root)
             
     except Exception as es:
         """messagebox.showerror(
             "Error", f"Due To :{str(es)}", parent=self.root)"""
             
 def get_cursor(self,event=""):
     cursor_row=self.AttendanceReportTable.focus()
     content=self.AttendanceReportTable.item(cursor_row)
     rows=content['values']
     self.var_atten_id.set(rows[0])   
     self.var_atten_roll.set(rows[1])
     self.var_atten_name.set(rows[2])
     self.var_atten_dep.set(rows[3])
     self.var_atten_time.set(rows[4])
     self.var_atten_date.set(rows[5])
     self.var_atten_attendance.set(rows[6])
     
     
     
 def reset_data(self):
     self.var_atten_id.set("")
     self.var_atten_roll.set("")
     self.var_atten_name.set("")
     self.var_atten_dep.set("")
     self.var_atten_time.set("")
     self.var_atten_date.set("")
     self.var_atten_attendance.set("")
     
 def fetch_database_data(self):
     conn = mysql.connector.connect(
         host="localhost", user="root", password="balu123", database="student_management")

     my_cursor = conn.cursor()
     my_cursor.execute("select * from attendance")
     data = my_cursor.fetchall()

     if len(data) != 0:
         self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
         for i in data:
             self.AttendanceReportTable.insert("", END, values=i)
         conn.commit()
     conn.close()

 def update(self):
     msg=''
     roll=self.var_atten_roll.get()
     name_str=self.var_atten_name.get()
     student_id=self.var_atten_id.get()
     time=self.var_atten_time.get()
     date=self.var_atten_date.get()
     
     if self.var_atten_attendance.get() == "Status" or self.var_atten_dep.get() == "Select Department" or self.var_atten_name.get() == "" or self.var_atten_id.get() == "" or self.var_atten_date.get() == "" or self.var_atten_time.get() == "" or self.var_atten_roll.get() == "":
         messagebox.showerror(
             "Error", "All Field are Required", parent=self.root)
         
     elif not any(ch.isdigit() for ch in student_id) :
         
         msg = 'Please Enter valid Attendance Id'
         messagebox.showerror(
             "Error", msg, parent=self.root)
     
     elif not any(ch.isdigit() for ch in roll):
         
         msg = 'Please Enter valid Roll number'
         messagebox.showerror(
             "Error", msg, parent=self.root)
         
     elif any(ch.isdigit() for ch in name_str):
         msg = 'Enter valid name'
         
         messagebox.showerror(
             "Error", msg, parent=self.root)
         
     elif not any(ch.isdigit() for ch in time) or any(ch.isalpha() for ch in time):
         msg = 'Please Enter valid Time'
         messagebox.showerror(
             "Error", msg, parent=self.root)
     elif not any(ch.isdigit() for ch in date) or any(ch.isalpha() for ch in date):
         msg = 'Please Enter valid date'
         messagebox.showerror(
             "Error", msg, parent=self.root)

         
         
         
     else:
         try:

             Update = messagebox.askyesno(
                 "update", "do you want to update this Attendance details", parent=self.root)
             if Update > 0:
                 conn = mysql.connector.connect(
                     host="localhost", user="root", password="balu123", database="student_management")

                 my_cursor = conn.cursor()
                 my_cursor.execute(
                     "update attendance set Roll=%s,Name=%s,Department=%s,Time=%s,Date=%s,Attendance=%s where AttendanceID=%s",(
                         self.var_atten_roll.get(),
                         self.var_atten_name.get(),
                         self.var_atten_dep.get(),
                         self.var_atten_time.get(),
                         self.var_atten_date.get(),
                         self.var_atten_attendance.get(),
                         self.var_atten_id.get()
                     ))
                 
             else:
                 if not Update:

                     return
                 
             messagebox.showinfo(
                 "success", "Attendance details successfully update completed", parent=self.root)
             conn.commit()
             self.fetch_database_data()
             self.reset_data()
             conn.close()
             
         except Exception as es:
             messagebox.showerror(
                 "Error", f"Due To : {str(es)}", parent=self.root)


#delete
 def delete(self):
     if self.var_atten_id.get() == "":
         messagebox.showerror(
             "Error", "Student id must be required", parent=self.root)

     else:
         try:

             delete = messagebox.askyesno(
                 "delete", "do you want to delete this Attendance details", parent=self.root)
             if delete > 0:
                 conn = mysql.connector.connect(
                     host="localhost", user="root", password="balu123", database="student_management")

                 my_cursor = conn.cursor()
                 sql = "delete from attendance where AttendanceID=%s"
                 val = (self.var_atten_id.get(),)
                 my_cursor.execute(sql, val)

             else:
                 if not delete:

                     return

             messagebox.showinfo(
                 "success", "Attendance details successfully deleted ", parent=self.root)
             conn.commit()
             self.fetch_database_data()
             self.reset_data()
             conn.close()

         except Exception as es:
             messagebox.showerror(
                 "Error", f"Due To : {str(es)}", parent=self.root)


  
  
  
  
  
  


if __name__ == "__main__":
    root = Tk()
    obj = attendance(root)
    root.mainloop()
