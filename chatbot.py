from tkinter import*
from tkinter import ttk
from turtle import left, title
from PIL import Image,ImageTk



class Chatbot:
 def __init__(self,root):
  self.root=root
  self.root.title("ChatBot")
  self.root.geometry("630x520+0+0")
  
  
  
  main_frame=Frame(self.root,bd=4,bg='powder blue',width=510)
  main_frame.pack()
  
  img_chat=Image.open('college_images/chat.jpg')
  img_chat=img_chat.resize((150,40),Image.ANTIALIAS)
  self.photoimg=ImageTk.PhotoImage(img_chat)
  
  title_lbl=Label(main_frame,bd=3,relief=RAISED,anchor='nw',width=620,compound=LEFT,image=self.photoimg,text='CHAT ME',font=('arial',20,'bold'),fg='green',bg='white')
  title_lbl.pack(side=TOP)
  
  
  
if __name__=='__main__':
 root=Tk()
 obj=Chatbot(root)
 root.mainloop()
  
