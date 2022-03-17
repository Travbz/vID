import tkinter as tk
from tkinter import*
from tkinter import filedialog, messagebox, ttk, simpledialog, font as tkFont

import pandas as pd

# initalise the tkinter GUI
root = tk.Tk()
root.title('vID')
root.tk.call('tk', 'windowingsystem') 
root.option_add('*tearOff', FALSE)
#getting screen width and height of display
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))
# set some global vars

# Frame for TreeView
frame1 = tk.LabelFrame(root, 
                    text="Unique ID Generator for .CSV and .XLSX",
                    font="ariel 30 bold")
frame1.pack(expand=True, fill='both', side='top')

# Frame for open file dialog
file_frame = tk.LabelFrame(root,
                    text="Open File", 
                    font="ariel 20 bold")
file_frame.pack(expand=True, ipady=100, fill='x', side='left')

# Buttons
singleIdBtn = tk.Button(file_frame,
                    bg= "grey16",
                    fg='linen',
                    text="SingleID",
                    command=lambda: openid(),
                    font="ariel 20 bold")
singleIdBtn.pack(side='left', padx=10, pady=5)

fileBrowserBtn = tk.Button(file_frame,
                    bg= "skyblue2",
                    text="Browse A File",
                    command=lambda: File_dialog(),
                    font="ariel 20 bold")
fileBrowserBtn.pack(side='left', padx=10, pady=5)

clearBtn = tk.Button(file_frame,
                    text='Clear Window',
                    bg= "coral3",
                    font="ariel 20 bold",
                    command=lambda: clear_data())
clearBtn.pack(side="left", padx=10, pady=5) 

saveBtn = tk.Button(file_frame,
                    text="Save As",
                    bg= "medium sea green",
                    font="ariel 20 bold",
                    command= lambda:save_excel(df))
saveBtn.pack(side="right", padx=10, pady=5)

generateIDBtn = tk.Button(file_frame,
                    text="Generate ID's",
                    bg= "wheat1", 
                    font="ariel 20 bold",
                    command=lambda: set_col_name())
generateIDBtn.pack(side="right", padx=10, pady=5) 

# The file/file path text
label_file = ttk.Label(file_frame,
                    text="No File Selected",
                    font="ariel 20 bold")
label_file.pack(side='top')

## Treeview Widget
style = ttk.Style()
style.configure("mystyle.Treeview",
                    highlightthickness=0,
                    bd=0,
                    font=('Calibri', 14)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading",
                    font=('Calibri',
                    14,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview",
                    [('mystyle.Treeview.treearea',
                    {'sticky': 'nswe'})]) # Remove the borders

tv1 = ttk.Treeview(frame1, style ="mystyle.Treeview" )
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

def File_dialog():
    root.update()
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes =(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = filename
    Load_excel_data()
# look to change file dialog box size https://bytes.com/topic/python/answers/908537-can-window-size-tffiledialog-changed
# also see: https://stackoverflow.com/questions/16429716/opening-file-tkinter

def Load_excel_data():
    global df
    global excel_filename
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    
    addCol(df)
    return df

def generate_unique_id(company_name: str) -> str:
    """
    :params company_name 
    :return a unique 12 character ID based on the named from the input  
    """
    global unique_key
    global company
    unique_key = ''
    company_name = company_name.upper()
    for char in (("THE ", ""), (" THE ", " "), (" AND ", " "), (" OF ", " ")):
        company_name = company_name.replace(*char)
        company = company_name
    new_name_list = []
    name_list = company_name.split(' ')
    wordCount = len(name_list)
    
    for name in name_list:
        new_name_list.append(''.join(ch for ch in name if ch.isalnum()))
    
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

    if len(unique_key) >= 8:
        unique_key = unique_key[0:8]
        
    elif len(unique_key) <= 8:
        unique_key += 'x' * (8 - len(unique_key))
    
    hash = 0    
    for ch in company_name:
        hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
    hash_number = str(hash)
    unique_key += hash_number[5:7]
    return unique_key

def keyList(df, columnName):
    keys_list = []
    for index, row in df.iterrows(): 
        keys_list.append(generate_unique_id(row[f"{columnName}"]))
    df['unique_ID'] = keys_list
    temp_cols=df.columns.tolist()
    new_cols=temp_cols[-1:] + temp_cols[:-1]
    df=df[new_cols]
    clear_data()   
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

def addCol(df):
    global variable
    # add dynamic list to append df col names to menu
    options = list(df.columns)
    # add menu
    variable = tk.StringVar(root)
    variable.set("Select Column Name")
    # Create the option_menu widget and passing 
    # the options and displayed to it.
    question_menu = tk.OptionMenu(file_frame, variable, *options)
    helv20 = tkFont.Font(family='Helvetica', size=20)
    menu = root.nametowidget(question_menu.menuname)
    menu.config(font=helv20)  # Set the dropdown menu's font
    question_menu.config(font="ariel 20 bold")
    question_menu.config(bg='azure') 
    question_menu.pack(side='left', padx=10, pady=5)

def set_col_name():
    col = variable.get()
    columnName = col
    keyList(df, columnName)
    return columnName

def save_excel(df):
    root.update()

    try:
        # with block automatically closes file
        with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name)
    except AttributeError:
        # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
        print("The user cancelled save")

# create function that passes input col name to gen_unique_id appends to df, clears treeview and replaces with updated df. save as option
# ideally buttons for select col name append after file load
def clear_data():
    tv1.delete(*tv1.get_children())
    return None
# function to open a new window
# on a button click

def openid():
    id = Toplevel(root)
    # Toplevel object which will
    # be treated as a new window
    id.title("vID")
    id.geometry('1400x650')

    # First labels
    myLabel = tk.Label(id,
                        text="Enter a name here",
                        font='Ariel 30 bold')
    myLabel.pack()
    myLabel2 = tk.Label(id, 
                        text="Please be sure the spelling is correct",
                        font='Ariel 20 bold')
    myLabel2.pack()

    # TextBox Creation
    inputtxt = tk.Text(id,
                    height = 3,
                    width = 60,
                    font='ariel 20 bold')
    inputtxt.pack()
    
    def gen_id() -> str:
        """
        :params company_name 
        :return a unique 12 character ID based on the named from the input
        """
        global unique_key
        global myID
        global whoamID
        unique_key = ''
        company_name = inputtxt.get(1.0, "end-1c")
        company_name = company_name.upper()
        for char in (("THE ", ""), (" THE ", " "), (" AND ", " "), (" OF ", " ")):
            company_name = company_name.replace(*char)
            company = company_name

        new_name_list = []
        name_list = company_name.split(' ')
        wordCount = len(name_list)
        
        for name in name_list:
            new_name_list.append(''.join(ch for ch in name if ch.isalnum()))
        
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

        if len(unique_key) >= 8:
            unique_key = unique_key[0:8]
            
        elif len(unique_key) <= 8:
            unique_key += 'x' * (8 - len(unique_key))
        
        hash = 0    
        for ch in company_name:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        hash_number = str(hash)
        unique_key += hash_number[5:7]
        myID = tk.Label(id,
                         text = "ID: " + unique_key,
                         font="ariel 20 bold")
        myID.pack()
        whoamID = tk.Label(id,
                             text= "Company: " + company,
                              font='ariel 20 bold')
        whoamID.pack()
        return unique_key

    #Define a function to clear the Entry Widget Content
    def clear_text():
        inputtxt.delete('1.0', 'end')
        myID.destroy()
        whoamID.destroy()
        copied.destroy()

    clearBtn = tk.Button(id, bg='navajowhite2',
                         text="Delete All",
                         command=lambda:clear_text(),
                         font=('Ariel 20 bold'))
    clearBtn.pack(side='bottom')
       
    # copy output to clipboard
    def copy():
        global copied
        id.clipboard_clear()
        # text to clipboard
        id.clipboard_append(unique_key)
        # text from clipboard
        clip_text = id.clipboard_get()
        copied = tk.Label(id,
                         text= f"Copied: {unique_key} to your clipboard.." ,
                          font='ariel 20 bold')
        copied.pack()
     
    def push_enter(inputtxt):
        gen_id()

    id.bind('<Return>', push_enter)

    # Button Creation
    name = str(inputtxt)
    genSingleIdBtn = tk.Button(id,
                            bg= "skyblue2",
                            text = "Generate ID", 
                            font="ariel 20 bold",
                            command =lambda: gen_id())
    genSingleIdBtn.pack(side='top')

    copyButton = tk.Button(id, 
                    bg="gold2",
                    text='Copy ID',
                    command=copy,
                    font="ariel 20 bold")
    copyButton.pack(side='top')

root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='images/ID.png'))

root.mainloop()
