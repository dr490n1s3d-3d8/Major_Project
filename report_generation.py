
from asyncore import read
import email
from operator import ge
from os import path
from time import time
from tkinter import *
import tkinter as tk
from tkinter import messagebox 
from jinja2 import Environment, FileSystemLoader
import fpdf
from matplotlib.pyplot import title
from numpy import pad
import pandas as pd 
from PIL import Image,ImageTk
import datetime
from ttkthemes import ThemedTk
from weasyprint import HTML,CSS
import webbrowser
import openpyxl


with open('result.txt','r') as result_file:
    result = result_file.read()

def save_patient_details():
    # import openpyxl module
    

    # Call a Workbook() function of openpyxl
    # to create a new blank Workbook object
    wb = openpyxl.Workbook("patients_details.xlsx")

    # Get workbook active sheet
    # from the active attribute
    sheet = wb.active

    # Cell objects also have row, column
    # and coordinate attributes that provide
    # location information for the cell.

    # Note: The first row or column integer
    # is 1, not 0. Cell object is created by
    # using sheet object's cell() method.
  

    # Once have a Worksheet object, one can
    # access a cell object by its name also.
    # A2 means column = 1 & row = 2.
    
    # Date = sheet['A2']
    # c3.value = "Welcome"

    # # B2 means column = 2 & row = 2.
    # c4 = sheet['B2']
    # c4.value = "Everyone"

    # # Anytime you modify the Workbook object
    # # or its sheets and cells, the spreadsheet
    # # file will not be saved until you call
    # # the save() workbook method.
    # wb.save("sample.xlsx")


def generate_report():
    if register_email.get() == "" or register_name == "" or register_mobile == "":
        messagebox.showwarning('Missing Fields ! ', 'Enter all details')
    else:
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template('./report_template.html')
        html = template.render(name=register_name.get(),
                        date=datetime.date.today() ,
                        gender =var.get(),
                        result=result,
                        age = 22 , 
                        doctor="Vincenzo Quassano",
                        lab=4
                        ) 
        with open(register_name.get()+' report.html', 'w') as f:
            f.write(html)
        with open("customer_history.txt","a") as history:
             history.writelines(f'\n\nDate : {datetime.date.today()}\nName : {register_name.get()}\nEmail : {register_email.get()}\nContact No : {register_mobile.get()}\nResult : {result}\n')
        css = CSS(string='''
        @page {size: A4; margin: 1cm;} 
        th, td {border: 1px solid black;}
        ''')
        HTML(register_name.get()+' report.html').write_pdf(register_name.get()+' report.pdf', stylesheets=[css])
        webbrowser.open((register_name.get()+' report.pdf'))



def stp_full(event=None):
    gen.attributes("-fullscreen", False)
    gen.geometry("1020x720")







gen =  ThemedTk(theme='equilux')
gen.title('Report Generation')
# gen.iconbitmap('.\Blood.ico')
gen.geometry('1920x1080')
gen.attributes("-fullscreen",True)

img = ImageTk.PhotoImage(Image.open("blood_report.png"))
label= Label(gen,image=img,width=1920,height=1080)
label.place(x=0,y=0,width=1920,height=1080)

# frame = Label(gen,bg='',width=1920,height=1080)
# frame.place(x=500,y=250,width=1920,height=1080)

f = ('Times', 14)
var = StringVar()
var.set('male')

image = Image.open("./Blood.jpg")
resize_image= image.resize((500,400))
img = ImageTk.PhotoImage(resize_image)

# report_logo_frame=Frame(
#     gen,
#     relief=SOLID,
#     
#     bd=2,
#     padx=10,
#     pady=10,
    
# )

patient_form = Frame(
    gen,
    padx=10, 
    pady=10
    )

gender_frame = LabelFrame(
    patient_form,
    
    padx=10, 
    pady=10,
    )


Label(
    patient_form, 
    text="Enter Patient Name", 
    
    font=f
    ).grid(row=0, column=0, sticky=W, pady=10)

Label(
    patient_form, 
    text="Enter Email", 
    
    font=f
    ).grid(row=1, column=0, sticky=W, pady=10)

Label(
    patient_form, 
    text="Contact Number", 
    
    font=f
    ).grid(row=2, column=0, sticky=W, pady=10)
Label(
    patient_form, 
    text="Select Gender", 
    
    font=f
    ).grid(row=3, column=0, sticky=W, pady=10)



register_name = Entry(
    patient_form, 
    font=f
    )

register_email = Entry(
    patient_form, 
    font=f
    )

register_mobile = Entry(
    patient_form, 
    font=f
    )

male_rb = Radiobutton(
    gender_frame, 
    text='Male',
    
    variable=var,
    value='male',
    font=('Times', 10),
    
)

female_rb = Radiobutton(
    gender_frame,
    text='Female',
    
    variable=var,
    value='female',
    font=('Times', 10),
  
)

others_rb = Radiobutton(
    gender_frame,
    text='Others',
    
    variable=var,
    value='others',
    font=('Times', 10)
   
)




register_name.grid(row=0, column=1, pady=10, padx=20)
register_email.grid(row=1, column=1, pady=10, padx=20) 
register_mobile.grid(row=2, column=1, pady=10, padx=20)
patient_form.place(x=500, y=250)

gender_frame.grid(row=3, column=1, pady=10, padx=20)
male_rb.pack(expand=True, side=LEFT)
female_rb.pack(expand=True, side=LEFT)
others_rb.pack(expand=True, side=LEFT)
# report_logo_frame.place(x=500,y=50)

image = Image.open("report_logo.png")
resize_image= image.resize((200,200))

img = ImageTk.PhotoImage(resize_image)
Label(
    gen,
    image=img
).place(x=600,y=50)
# Generate Button ##

generate_btn = tk.Button(gen,text='Generate Report',command=generate_report)
generate_btn.place(x=650, y=575)
exit_btn = tk.Button(gen,text='Close',command=lambda:gen.destroy())
exit_btn.place(x=800, y=575)

gen.bind("<Escape>", stp_full)
gen.mainloop()
