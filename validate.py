from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def mob_email_validation():
    special_ch = ['@', '.']
    msg = ''
    me = mob_email.get()
    if me == '':
        msg = 'provide Mobile num or Email'
    else:
        try:
            if any(ch.isdigit() for ch in me):
                if len(me) == 10:
                    mob = int(me)
                    msg = 'success'
                else:
                    msg = 'incorrect mobile number!'
            else:
                if not any(ch in special_ch for ch in me):
                    msg = 'incorrect email!'
                else:
                    msg = 'success!'
        except Exception as ep:
            msg = ep
    messagebox.showinfo('message', msg)


def validation(name_str, elm):
    msg = ''
    if name_str == '':
        msg = f'{elm} is required!'
    else:
        try:
            if len(name_str) == 0:
                msg = 'Name is too small'
            elif any(ch.isdigit() for ch in name_str):
                msg = 'Name cannot have numbers'
            else:
                msg = f'success for {elm}'
        except Exception as ep:
            messagebox.showerror('message', ep)
    messagebox.showinfo('message', msg)


def btn_clicked():

    validation(fname.get(), 'first name')
    validation(surname.get(), 'last name')
    mob_email_validation()


def on_click_fname(event):
    fname.configure(state=NORMAL)
    fname.delete(0, END)
    fname.unbind('<Button-1>', on_click_id1)


def on_click_surname(event):
    surname.configure(state=NORMAL)
    surname.delete(0, END)
    surname.unbind('<Button-1>', on_click_id2)


def on_click_mob_email(event):
    mob_email.configure(state=NORMAL)
    mob_email.delete(0, END)
    mob_email.unbind('<Button-1>', on_click_id3)


def disp_date(choice):
    choice = day_var.get()
    print(choice)


def disp_month(choice):
    choice = month_var.get()
    print(choice)


def disp_year(choice):
    choice = year_var.get()
    print(choice)


ws = Tk()
ws.title('PythonGuides')
ws.geometry('600x600')
ws.config(bg='#fff')

firstname = StringVar()
username = StringVar()
password = StringVar()
day = [x for x in range(1, 32)]
month = [x for x in range(1, 13)]
year = [x for x in range(1905, 2022)]

# print(date)
# print(month)
# print(year)

Label(
    ws,
    text='Sign Up',
    font=('sans-serif', 32),
    bg='#fff'
).grid(row=0, columnspan=2, sticky='EW')

Label(
    ws,
    text='It\'s quick and easy',
    font=('sans-serif', 15),
    fg='#606770',
    bg='#fff',
).grid(row=1, columnspan=2, sticky='EW')

Label(
    ws,
    text='_'*85,
    fg='#ccd065',
    bg='#fff',
).grid(row=2, columnspan=2, pady=(0, 20))

fname = Entry(
    ws,
    bg='#fff',
    font=('sans-serif', 15)
)
fname.grid(row=3, column=0, pady=(0, 10))

surname = Entry(
    ws,
    bg='#fff',
    font=('sans-serif', 15),
)
surname.grid(row=3, column=1, pady=(0, 10))

mob_email = Entry(
    ws,
    bg='#fff',
    font=('sans-serif', 15),
    width=43
)
mob_email.grid(row=4, columnspan=2, pady=(0, 10))

# adding placeholders
fname.insert(0, 'First name')
fname.configure(state=DISABLED)
surname.insert(0, 'Surname')
surname.configure(state=DISABLED)
mob_email.insert(0, 'Mobile number or email address')
mob_email.configure(state=DISABLED)

# binding placeholders
fname.bind('<Button-1>', on_click_fname)
surname.bind('<Button-1>', on_click_surname)
mob_email.bind('<Button-1>', on_click_mob_email)

on_click_id1 = fname.bind('<Button-1>', on_click_fname)
on_click_id2 = surname.bind('<Button-1>', on_click_surname)
on_click_id3 = mob_email.bind('<Button-1>', on_click_mob_email)


dob = LabelFrame(
    ws,
    text='Date of birth',
    font=('sans-serif', 12),
    bg='#fff',
    padx=10,
    pady=10
)
dob.grid(row=5, columnspan=2, sticky='EW', padx=18, pady=(0, 10))

day_var = IntVar()
month_var = StringVar()
year_var = StringVar()

# display defaults
day_var.set(day[7])
month_var.set(month[3])
year_var.set(year[-1])

day_cb = ttk.Combobox(
    dob,
    textvariable=day_var,
    font=('sans-serif', 15),
    width=12,
    background=['#fff']  # ToDo
)
day_cb.grid(row=6, column=0, padx=(0, 15), ipady=10)

month_cb = ttk.Combobox(
    dob,
    textvariable=month_var,
    font=('sans-serif', 15),
    width=12
)
month_cb.grid(row=6, column=1, padx=(0, 15), ipady=10)


year_cb = ttk.Combobox(
    dob,
    textvariable=year_var,
    font=('sans-serif', 15),
    width=12
)
year_cb.grid(row=6, column=2, ipady=10)

day_cb['values'] = day
month_cb['values'] = month
year_cb['values'] = year

# disable editing
day_cb['state'] = 'readonly'
month_cb['state'] = 'readonly'
year_cb['state'] = 'readonly'

gender = Frame(
    ws,
    bg='#fff',
)
gender.grid(row=7, columnspan=2)

gen_var = IntVar()
gen_var.set(1)

female_rb = Radiobutton(
    gender,
    text='Female',
    bg='#fff',
    variable=gen_var,
    value=1,
    font=('sans-serif', 15),
    anchor='w'
)
female_rb.pack(fill=BOTH, expand=True, side=LEFT,
               padx=10, pady=10, ipadx=10, ipady=10)

male_rb = Radiobutton(
    gender,
    text='Male',
    bg='#fff',
    variable=gen_var,
    value=2,
    font=('sans-serif', 15),
    anchor='w'
)
male_rb.pack(fill=BOTH, expand=True, side=LEFT,
             padx=10, pady=10, ipadx=25, ipady=10)

custom_rb = Radiobutton(
    gender,
    text='Others',
    bg='#fff',
    variable=gen_var,
    value=3,
    font=('sans-serif', 15),
    anchor='w'
)
custom_rb.pack(expand=True, fill=BOTH, side=LEFT,
               padx=10, pady=10, ipadx=10, ipady=10)

terms = '''
By clicking Sign Up, you agree to our Terms, Data Policy and Cookie Policy. You may receive SMS notifications from us and can opt out at any time.
'''
Label(
    ws,
    text=terms,
    wraplength=500,
    bg='#fff'

).grid(row=8, columnspan=2)

signup_btn = Button(
    ws,
    text='Sign Up',
    command=btn_clicked,  # ToDo
    font=('sans-serif', 18),
    padx=40,
    pady=10,
)
signup_btn.grid(row=9, columnspan=2)

ws.mainloop()
