from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

from main import face_recognization_system
    
def main():
    win=Tk()
    app=Login(win)
    win.mainloop()
    
    


class Login:
 def __init__(self, root):
  self.root = root
  self.root.title("Login window")
  self.root.geometry("1350x700+0+0")
  
  imgb = Image.open(r"college_images\modernnew.jpg")
  imgbg = imgb.resize((1500, 800), Image.ANTIALIAS)
  self.photoimgbg = ImageTk.PhotoImage(imgbg)
  lbl_bg = Label(self.root, image=self.photoimgbg)
  lbl_bg.place(x=0, y=0, width=1500, height=800)
  
  
  
  #=============== frame
  bg_frame=Frame(self.root,bg="black")
  bg_frame.place(x=530,y=150,width=300,height=450)
  
  
  img1 = Image.open(
      r"college_images\LoginIconAppl.png")
  img1 = img1.resize((100, 100), Image.ANTIALIAS)
  self.photoimg3 = ImageTk.PhotoImage(img1)
  img_lbl = Label(self.root, image=self.photoimg3,bg="black",borderwidth=0)
  img_lbl.place(x=630, y=155, width=100, height=100)
  
  
  get_str=Label(bg_frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
  get_str.place(x=80,y=100)
  
  
  
  #====label
  
  username = Label(bg_frame, text="Username", font=(
      "times new roman", 15, "bold"), fg="white", bg="black")
  username.place(x=60,y=160)
  
  self.textuser = ttk.Entry(bg_frame, font=(
      "times new roman", 15, "bold"))
  self.textuser.place(x=30, y=190,width=240)
  
  
  password = Label(bg_frame, text="Password", font=(
      "times new roman", 15, "bold"), fg="white", bg="black")
  password.place(x=60, y=220)

  self.textpass = ttk.Entry(bg_frame,show='*', font=(
      "times new roman", 15, "bold"))
  self.textpass.place(x=30, y=250, width=240)
  
  
  #======icon
  
  img2 = Image.open(
      r"college_images\LoginIconAppl.png")
  img2 = img2.resize((25, 25), Image.ANTIALIAS)
  self.photoimg2 = ImageTk.PhotoImage(img2)
  img_lbl = Label(self.root, image=self.photoimg2, bg="black", borderwidth=0)
  img_lbl.place(x=565, y=310, width=25, height=25)
  
  
  img3 = Image.open(
      r"college_images\Lock-512.png")
  img3 = img3.resize((25, 25), Image.ANTIALIAS)
  self.photoimg1 = ImageTk.PhotoImage(img3)
  img_lbl = Label(self.root, image=self.photoimg1, bg="black", borderwidth=0)
  img_lbl.place(x=565, y=375, width=25, height=25)
  
  
  
  
  #========== login button
  
  login_button = Button(bg_frame, text="Login",command=self.login, font=(
      "times new roman", 15, "bold"),bd=3,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
  login_button.place(x=80,y=300,width=120,height=35)
  
  #========== register button

  register_button = Button(bg_frame,command=self.register_window, text="New User Register", font=(
      "times new roman", 10, "bold"),borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
  register_button.place(x=15, y=350, width=150)
  
  #========== forgot button

  forgot_button = Button(bg_frame, text="Forget Password", font=(
      "times new roman", 10, "bold"),command=self.forgot_passsword_window, borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
  forgot_button.place(x=10, y=370, width=150)
  
  
  
 def register_window(self):
    self.new_window=Toplevel(self.root)
    self.app=Register(self.new_window)
  
 #===========Function
 
 def login(self):
     
     
     if self.textuser.get()=="" or self.textuser.get()=="":
         messagebox.showerror("Error","all field required")
         
     elif self.textuser.get()=="bala" and self.textpass.get()=="bala":
         messagebox.showinfo("Success","Welcome ")
             
     else:
         conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123", database="mydata")
         my_cursor = conn.cursor()
         my_cursor.execute("select * from register where email=%s and password=%s",(
             self.textuser.get(),
             self.textpass.get()
             
                                                                                   ))
         
         row=my_cursor.fetchone()
         if row==None:
             messagebox.showerror("Error","Invalid username and password")
             
         else:
             self.new_window = Toplevel(self.root)
             self.app = face_recognization_system(self.new_window)
             
         conn.commit()
         conn.close()
         
#======================reset pass============================

 def reset_pass(self):
     if self.combo_security.get()==("Select"):
         messagebox.showerror(
             "Error", "Select the security Quetion", parent=self.root2)
     elif self.security_text.get()=="":
         messagebox.showerror(
             "Error", "Please enter the answer", parent=self.root2)
     elif self.txt_new_password.get()=="":
         messagebox.showerror(
             "Error", "Please enter the new password", parent=self.root2)
         
     else:
         conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123", database="mydata")
         my_cursor = conn.cursor()
         query=("select * from register where email=%s and securityQ=%s and securityA=%s")
         value=(self.textuser.get(),self.combo_security.get(),self.security_text.get())
         my_cursor.execute(query,value)
         row=my_cursor.fetchone()
         if row==None:
             messagebox.showerror(
                 "Error", "please enter the correct security  answer", parent=self.root2)
             
         else:
             query=("update register set password=%s where email=%s")
             value=(self.txt_new_password.get(),self.textuser.get())
             my_cursor.execute(query,value)
             messagebox.showinfo(
                 "info", "your password has been reset  ", parent=self.root2)
             conn.commit()
             conn.close()
             self.root2.destroy()
             
         
#=================== return login from registation window==





#=========================forgot passs=====================
 def forgot_passsword_window(self):
     if self.textuser.get()=="":
         messagebox.showerror("Error","Please enter the email address to reset password")
         
     else:
         conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123", database="mydata")
         my_cursor = conn.cursor()
         query=("select * from register where email=%s")
         value=(self.textuser.get(),)
         my_cursor.execute(query,value)
         row=my_cursor.fetchone()
         
         if row==None:
             messagebox.showerror("Error","Please enter the valid user name")
             
         else:
             conn.close()
             self.root2=Toplevel()
             self.root2.title("Forgot Password")
             self.root2.geometry("400x455+500+140")
             lbl = Label(self.root2, text="Forgot Password", font=(
                 "times new roman", 15, "bold"), borderwidth=0, fg="red", bg="white")
             lbl.place(x=0,y=10,relwidth=1)
             
             
             security = Label(self.root2, text="Select Security Quations", font=(
                "times new romen", 15, "bold"), bg="white")
             security.place(x=40, y=60)

             self.combo_security = ttk.Combobox(self.root2, font=(
                "times new roman", 15, "bold"), state="readonly")
             self.combo_security["values"] = (
                "Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name")
             self.combo_security.current(0)
             self.combo_security.place(x=40, y=100)

             security_A = Label(self.root2, text="Select Security Answer", font=(
                "times new romen", 15, "bold"), bg="white", fg="black")
             security_A.place(x=40, y=140)
             self.security_text = ttk.Entry(self.root2, font=(
                "times new roman", 15, "bold"))
             self.security_text.place(x=40, y=180, width=230)    
             
             new_password = Label(self.root2, text="New Password", font=(
                 "times new romen", 15, "bold"), bg="white", fg="black")
             new_password.place(x=40, y=220)
             self.txt_new_password = ttk.Entry(self.root2,show='*', font=(
                 "times new roman", 15, "bold"))
             self.txt_new_password.place(x=40, y=260, width=230)
             
             btn1 = Button(self.root2, text="Reset",command=self.reset_pass, font=(
                 "times new roman", 10, "bold"), borderwidth=0, fg="white", bg="green")
             btn1.place(x=40,y=320)

         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
             
         
class Register:
 def __init__(self, root1):
  self.root1 = root1
  self.root1.title("Registeration window")
  self.root1.geometry("1550x800+0+0")


  #============ varible============

  self.var_fname = StringVar()
  self.var_lname = StringVar()
  self.var_contact = StringVar()
  self.var_email = StringVar()
  self.var_securityQ = StringVar()
  self.var_securityA = StringVar()
  self.var_pass = StringVar()
  self.var_confpass = StringVar()

  self.bg = ImageTk.PhotoImage(
      file=r"college_images\Windows 10 Spotlight Images1.png")
  lbl_bg = Label(self.root1, image=self.bg)
  lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
  #left img
  self.bg1 = ImageTk.PhotoImage(
      file=r"college_images\thought-good-morning-messages-LoveSove.jpg")
  lbl_bg1 = Label(self.root1, image=self.bg1)
  lbl_bg1.place(x=50, y=50, width=450, height=550)

  #    ============ main  frame============================

  frame = Frame(self.root1, bg="white")
  frame.place(x=500, y=50, width=600, height=550)

  register_lbl = Label(frame, text="REGISTER HERE", font=(
      "times new romen", 20, "bold"), fg="darkgreen", bg="white")
  register_lbl.place(x=10, y=10)

  #==================labes and entry=====================

  fname = Label(frame, text="First Name", font=(
      "times new romen", 15, "bold"), bg="white")
  fname.place(x=40, y=80)
  self.fname = ttk.Entry(frame, textvariable=self.var_fname, font=(
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
      "times new roman", 15, "bold"), state="readonly")
  self.combo_security["values"] = (
      "Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name")
  self.combo_security.current(0)
  self.combo_security.place(x=40, y=280)

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
  self.password = ttk.Entry(frame, textvariable=self.var_pass,show='*', font=(
      "times new roman", 15, "bold"))
  self.password.place(x=40, y=380, width=230)

  conform_passd = Label(frame, text="Conform Password", font=(
      "times new romen", 15, "bold"), bg="white")
  conform_passd.place(x=300, y=330)
  self.conform_passd = ttk.Entry(frame, textvariable=self.var_confpass,show='*', font=(
      "times new roman", 15, "bold"))
  self.conform_passd.place(x=300, y=380, width=230)

  #=========================checkbutton
  self.var_check = IntVar()

  check_btn = Checkbutton(frame, variable=self.var_check, text="I Agree The Terms & Condition ", onvalue=1, offvalue=0, bg="white", fg="black", font=(
      "times new roman", 11, "bold"))
  check_btn.place(x=40, y=420)


#=======Button===============
  
  b1 = Button(frame, command=self.register_data,
              text="Register", borderwidth=0, fg="pink", font=("times new roman", 18, "bold"), bg="darkgreen", cursor="hand2")
  b1.place(x=230, y=480, width=95, height=35)

  
  """b2 = Button(frame, command=self.return_login,
              text="Login", borderwidth=0, fg="pink", font=("times new roman", 20, "bold"), bg="red", cursor="hand2")
  b2.place(x=310, y=480, width=90,height=35)

 def return_login(self):

     self.root1.destroy()"""
     
 def checkpass(self, password):
     if len(password) <= 20:
         return True
     else:
         messagebox.showerror(
             "Invalid", "password lenth should be less than 20 character")

 def checkname(self, name):
     if name.isalnum():
         return True
     if len(int(name)) == 0:
         return True

     if name == '':
         return True

     else:
         messagebox.showerror('Invalid', 'Enter Valid Allowed')
         return False

 def checkemail(self, email):
     special_char = ['@', '.']
     if email in special_char:
         return True

     else:
         messagebox.showerror("Invalid", "Email should contain @ and .")
         
 def checkcontact(self, contact):

     if contact.isdigit() or contact == ':':
         return True
     elif len(str(contact)) == 0:
         return True
     #elif  contact ==':':
         #return True

     else:
         messagebox.showerror("Invalid", "Invalid Entry")
         return False


#===================function declaration

 def register_data(self):
     special_ch=['@','.']
     email=self.var_email.get()
     phone=self.var_contact.get()
     name_str=self.var_fname.get()
     last_str=self.var_lname.get()
     
     
     if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_lname.get() == "" or self.var_pass.get() == "" or self.var_confpass.get() == "" or self.var_securityA.get() == "" or self.var_contact.get() == "" or self.var_securityQ.get() == "Select":
         messagebox.showerror(
             "Error", "All fields are required", parent=self.root1)
         
     elif any(ch.isdigit() for ch in name_str):
         msg = 'Please Enter valid First Name'
         messagebox.showerror(
             "Error", msg, parent=self.root1)
         
     elif any(ch.isdigit() for ch in last_str):
         msg = 'Please Enter valid Last Name'
         messagebox.showerror(
             "Error", msg, parent=self.root1)
     elif not any(ch.isdigit() for ch in phone)  :
         msg = 'Please Enter valid number'
         messagebox.showerror(
             "Error", msg, parent=self.root1)
     elif  len(phone) != 10:
         msg = 'Please Enter 10 digit number'
         messagebox.showerror(
             "Error", msg, parent=self.root1)
     elif not any(ch in special_ch for ch in email):
         msg = 'Please Enter valid email!'
         messagebox.showerror(
             "Error", msg, parent=self.root1)
         
     elif self.var_pass.get() != self.var_confpass.get():
         messagebox.showerror(
             "Error", "password $ confirm password must be same", parent=self.root1)

     elif self.var_check.get() == 0:
         messagebox.showerror(
             "Error", "Please agree our terms and condition ", parent=self.root1)
     
     
     else:
         conn = mysql.connector.connect(
             host="localhost", user="root", password="balu123", database="mydata")
         my_cursor = conn.cursor()
         quary = ("select * from register where email=%s")
         value = (self.var_email.get(),)
         my_cursor.execute(quary, value)
         row = my_cursor.fetchone()
         if row != None:
             messagebox.showerror(
                 "Error", "User already exist,please try another email", parent=self.root1)
         else:
             my_cursor.execute(
                 "insert into register values(%s,%s,%s,%s,%s,%s,%s)", (
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
         messagebox.showinfo("Success", "Register Successfully",parent=self.root1)
         self.root1.destroy()
         
         
         
         
         
         
         
#========================== Project==============================



  #===============Function  buttion========

 






if __name__ == "__main__":
    
    main()

 


