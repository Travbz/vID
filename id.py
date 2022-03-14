import tkinter as tk
from tkinter import *

# Top level window
frame = tk.Tk()
frame.title("vID")
frame.geometry('1400x650')

# First labels
myLabel = tk.Label(frame, text="Enter a name here", font='Ariel 30 bold')
myLabel.pack()
myLabel2 = tk.Label(frame, text="Please be sure the spelling is correct", font='Ariel 20 bold')
myLabel2.pack()

# TextBox Creation
inputtxt = tk.Text(frame,
                   height = 3,
                   width = 60,
                   font='ariel 20 bold')
inputtxt.pack()

# slice unique id
def generate_unique_id() -> str:
    """
    :params company_name 
    :return an ID based on the name from the input
    """
    global unique_key
    unique_key = ''
    company_name = inputtxt.get(1.0, "end-1c")
    company_name = company_name.upper()
    
    # remove designated 'stop' words from name
    for char in (("THE ", ""), (" THE ", " "), (" AND ", " "), (" OF ", " ")):
        company_name= company_name.replace(*char)
        company = company_name
    name_list = company_name.split(' ')
    wordCount = len(name_list)
    new_name_list = []

    for name in name_list:
        new_name_list.append(''.join(ch.upper() for ch in name if ch.isalnum()))
    
    if wordCount == 1:
        unique_key = new_name_list[0][0:8]
    else:
        for i in range(len(new_name_list)):
            if i == 0:
                unique_key += new_name_list[i][:4]
            else:
                unique_key += new_name_list[i][:2]

            if len(unique_key) > 7:
                break
    
    if len(unique_key) <= 8:
        unique_key += 'x' * (8 - len(unique_key))
        
    hash = 0    
    for ch in unique_key:
        hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
    hash_number = str(hash)
    
    unique_key += hash_number[0:3]

    lbl.config(text = "ID: " + unique_key, font="ariel 20 bold")
    lbl2.config(text= "Company: " + company, font='ariel 20 bold')

# copy output to clipboard
def copy():
    frame.clipboard_clear()
    # text to clipboard
    frame.clipboard_append(unique_key)
    # text from clipboard
    clip_text = frame.clipboard_get()
    lbl3.config(text= f"Copied: {unique_key} to your clipboard.." , font='ariel 20 bold')
    print(f'Unique Key Copied to clipboard', clip_text)

#Define a function to clear the Entry Widget Content
def clear_text():
   inputtxt.delete('1.0', 'end')
   generate_unique_id()
   
clear = tk.Button(frame, bg='light yellow', text="Delete All", command=clear_text, font=('Ariel 20 bold')).pack(side='bottom')

# Button Creation
printButton = tk.Button(frame,
                        bg= "light blue",
                        text = "Generate ID", 
                        font="ariel 20 bold",
                        command = generate_unique_id)
printButton.pack(side='top')

copyButton = tk.Button(frame, 
                bg="yellow",
                text='Copy Id',
                command=copy,
                font="ariel 20 bold")
copyButton.pack(side='top')

# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()
lbl2 = tk.Label(frame, text = "")
lbl2.pack()
lbl3 = tk.Label(frame, text = "")
lbl3.pack()

frame.tk.call('wm', 'iconphoto', frame._w, tk.PhotoImage(file='images/ID.png'))

# run loop
frame.mainloop()

