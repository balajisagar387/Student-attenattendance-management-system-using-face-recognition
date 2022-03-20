from cgitb import text
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector


class Register :
 def __init__(self,root):
  self.root=root
  self.root.title("Registeration window")
  self.root.geometry("1550x800+0+0")
  
  
  
  #============ varible============
  
  self.var_fname=StringVar()
  self.var_lname = StringVar()
  self.var_contact = StringVar()
  self.var_email = StringVar()
  self.var_securityQ = StringVar()
  self.var_securityA = StringVar()
  self.var_pass = StringVar()
  self.var_confpass = StringVar()
  
  
  
  self.bg = ImageTk.PhotoImage(
      file=r"C:\Users\Birajdar balaji\OneDrive\Desktop\student management system\college_images\Windows 10 Spotlight Images1.png")
  lbl_bg = Label(self.root,image=self.bg)
  lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
  #left img
  self.bg1 = ImageTk.PhotoImage(
      file=r"C:\Users\Birajdar balaji\OneDrive\Desktop\student management system\college_images\thought-good-morning-messages-LoveSove.jpg")
  lbl_bg1 = Label(self.root, image=self.bg1)
  lbl_bg1.place(x=50, y=50, width=450, height=550)
  
  
  #    ============ main  frame============================
  
  frame=Frame(self.root,bg="white")
  frame.place(x=500,y=50,width=600,height=550)
  
  register_lbl=Label(frame,text="REGISTER HERE",font=("times new romen",20,"bold"),fg="darkgreen",bg="white")
  register_lbl.place(x=10,y=10)
  
  
  #==================labes and entry=====================
  
  fname = Label(frame, text="First Name", font=("times new romen", 15, "bold"),bg="white")
  fname.place(x=40,y=80)
  self.fname = ttk.Entry(frame,textvariable=self.var_fname, font=(
      "times new roman", 15, "bold"))
  self.fname.place(x=40, y=110, width=230)
  
  lname = Label(frame, text="Last Name", font=(
      "times new romen", 15, "bold"), bg="white")
  lname.place(x=300, y=80)
  self.lname = ttk.Entry(frame, textvariable=self.var_lname, font=(
      "times new roman", 15, "bold"))
  self.lname.place(x=300, y=110, width=230)
  # ============= row2
  contact = Label(frame, text="Contact No", font=(
      "times new romen", 15, "bold"), bg="white")
  contact.place(x=40, y=150)
  self.contact = ttk.Entry(frame, textvariable=self.var_contact, font=(
      "times new roman", 15, "bold"))
  self.contact.place(x=40, y=180, width=230)

  email = Label(frame, text="Email", font=(
      "times new romen", 15, "bold"), bg="white")
  email.place(x=300, y=150)
  self.email = ttk.Entry(frame, textvariable=self.var_email, font=(
      "times new roman", 15, "bold"))
  self.email.place(x=300, y=180, width=230)
  
  
  
  #==============row 3=============
  
  security = Label(frame, text="Select Security Quations", font=(
      "times new romen", 15, "bold"), bg="white")
  security.place(x=40, y=230)
  
  self.combo_security = ttk.Combobox(frame, textvariable=self.var_securityQ, font=(
      "times new roman", 15, "bold"),state="readonly")
  self.combo_security["values"]=("Select","Your Birth Place","Your Girlfriend Name","Your Pet Name")
  self.combo_security.current(0)
  self.combo_security.place(x=40,y=280)
  
  security_A = Label(frame, text="Select Security Answer", font=(
      "times new romen", 15, "bold"), bg="white", fg="black")
  security_A.place(x=300, y=230)
  self.security_text = ttk.Entry(frame, textvariable=self.var_securityA, font=(
      "times new roman", 15, "bold"))
  self.security_text.place(x=300, y=280, width=230)
  
  #============row 4===============
  password = Label(frame, text="Password", font=(
      "times new romen", 15, "bold"), bg="white")
  password.place(x=40, y=330)
  self.password = ttk.Entry(frame, textvariable=self.var_pass, font=(
      "times new roman", 15, "bold"))
  self.password.place(x=40, y=380, width=230)

  conform_passd = Label(frame, text="Conform Password", font=(
      "times new romen", 15, "bold"), bg="white")
  conform_passd.place(x=300, y=330)
  self.conform_passd = ttk.Entry(frame, textvariable=self.var_confpass, font=(
      "times new roman", 15, "bold"))
  self.conform_passd.place(x=300, y=380, width=230)
  
  
  
  
  #=========================checkbutton
  self.var_check = IntVar()
  
  check_btn = Checkbutton(frame, variable=self.var_check, text="I Agree The Terms & Condition ", onvalue=1, offvalue=0, bg="white", fg="black", font=(
      "times new roman", 11, "bold"))
  check_btn.place(x=40,y=420)
  
  
#=======Button===============
  img = Image.open(r"C:\Users\Birajdar balaji\OneDrive\Desktop\student management system\college_images\register-now-button1.jpg")
  img=img.resize((80,40),Image.ANTIALIAS)
  self.photoimg=ImageTk.PhotoImage(img)
  b1=Button(frame,image=self.photoimg,borderwidth=0,command=self.register_data,cursor="hand2")
  b1.place(x=40,y=460,width=250)
  
  
  img1 = Image.open(
      r"C:\Users\Birajdar balaji\OneDrive\Desktop\student management system\college_images\index11.jpg")
  img = img1.resize((10, 40), Image.ANTIALIAS)
  self.photoimg1 = ImageTk.PhotoImage(img1)
  b1 = Button(frame, image=self.photoimg1, borderwidth=0, cursor="hand2")
  b1.place(x=310, y=460, width=250)
  
  
  
  
#===================function declaration
 def register_data(self):
     if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_securityQ.get() == "Select":
         messagebox.showerror("Error","All fields are required")
     elif self.var_pass.get()!=self.var_confpass.get():
         messagebox.showerror("Error","password $ confirm password must be same")
         
     elif self.var_check.get()==0:
         messagebox.showerror("Error","Please agree our terms and condition ")
     else:
         conn=mysql.connector.connect(host="localhost",user="root",password="balu123",database="mydata")
         my_cursor=conn.cursor()
         quary=("select * from register where email=%s")
         value=(self.var_email.get(),)
         my_cursor.execute(quary,value)
         row=my_cursor.fetchone()
         if row!=None:
             messagebox.showerror("Error","User already exist,please try another email")
         else:
             my_cursor.execute(
                 "insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                 self.var_fname.get(),
                 self.var_lname.get(),
                 self.var_contact.get(),
                 self.var_email.get(),
                 self.var_securityQ.get(),
                 self.var_securityA.get(),
                 self.var_pass.get()
                 
                             ))
         conn.commit()
         conn.close()
         messagebox.showinfo("Success","Register Successfully")
         
             
         
         
         
         
         
  
  
  
  

  

  

     
if __name__=="__main__":    
  
  root=Tk()
  obj=Register(root)
  root.mainloop()

 