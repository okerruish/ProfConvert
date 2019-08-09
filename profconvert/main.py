import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox
import csv  
import json
import sys
import subprocess
import pandas as pd
import os
from tkinter.filedialog import askdirectory

#Imports the CSV data document the client gets from their website using a Google Form format provided.
def importCSV():
        global initial
        initial = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Files",".csv")])
        #Clears all values to insert "null" which the 3rd party software takes
        maincsv=pd.read_csv(initial)
        maincsv=maincsv.fillna('')
        #Shows user the file path of imported csv
        T.delete(1.0, tk.END)
        T.insert(tk.END, "File path: " +str(initial))
#Formats the CSV data document into nested JSON for use in 3rd party software
def exportJSON():
        #Opens the CSV with alias data_file
        with open(initial, 'r') as data_file:
                reader = csv.reader(data_file)
                #Skips header row
                next(reader)
                #Defines dictionary to write json to.
                all_records = []
                #Loops over every row
                for row in reader:
                        #If statement to choose different formatting if user has billing address or not.
                        if row[21] == '':
                                row_data_dict = {"name":row[0],"email":row[1],"phone":row[15],"sizes":[],"taskAmount":1,"singleCheckout":True,"billingDifferent":False,"favorite":False,"card":{"number":row[5],"expiryMonth":row[7],"expiryYear":row[8],"cvv":row[6]},"delivery":{"firstName":row[9],"lastName":row[10],"address1":row[16],"address2":row[17],"zip":row[13],"city":row[12],"country":row[11],"state":row[14]},"billing":{"firstName":None,"lastName":None,"address1":None,"address2":None,"zip":None,"city":None,"country":None,"state":None}}
                                all_records.append(row_data_dict)
                        else:
                                row_data_dict = {"name":row[0],"email":row[1],"phone":row[15],"sizes":[],"taskAmount":1,"singleCheckout":True,"billingDifferent":True,"favorite":False,"card":{"number":row[5],"expiryMonth":row[7],"expiryYear":row[8],"cvv":row[6]},"delivery":{"firstName":row[20],"lastName":row[21],"address1":row[27],"address2":row[28],"zip":row[24],"city":row[23],"country":row[22],"state":row[25]},"billing":{"firstName":row[9],"lastName":row[10],"address1":row[16],"address2":row[17],"zip":row[13],"city":row[12],"country":row[11],"state":row[14]}}
                                all_records.append(row_data_dict)
        #Writes the formatted JSON to a file in a user specified destination
        j = json.dumps(all_records)
        out = filedialog.asksaveasfilename(defaultextension=".json",filetypes=[('JSON files', '.json')])
        #Opens the file specified in "write" mode and prints the all_records dictionary.
        f = open(out, 'w')
        print(j, file=f)
        def success():
            messagebox.showinfo(title="Export Success", message="The .json file was exported successfully.")
        success()
        f.close()

#Defines the class for the Page module
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        

class Page1(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        #Sets background colour of page
        label = tk.Label(self, background="#0d0922")
        label.pack(side="top", fill="both", expand=True)
        #Adds the Heading and buttons to the page
        title = tk.Label(self, text="Profile Converter", font=("Helvetica Neue LT Com 93 Black Extended Oblique", 24), fg="#d402d7", bg="#0d0922")
        btnImportCSV = tk.Button(self, text="Import CSV", highlightbackground="#0d0922", foreground="#d402d7", background="#ffe600", font=('Helvetica Neue', 16), width=10, command=importCSV)
        btnExportJSON = tk.Button(self, text="Export", highlightbackground="#0d0922", foreground="#d402d7", background="#ffe600", font=('Helvetica Neue', 16), width=10, command=exportJSON)
        global T
        #Creates the text box to be updated with selected file path
        T = tk.Text(self, height=3, width=36, fg="#ffe600", bg="#0d0922", font=("Helvetica Neue", 16))
        T.insert(tk.END, "No file selected.")
        title.place(relx=0.23, rely=0.06)
        btnImportCSV.place(relx=0.4, rely=0.25)
        btnExportJSON.place(relx=0.4, rely=0.75)
        T.place(relx=0.22, rely=0.44)

class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        ok = tk.Label(self, background="#0d0922")
        ok.pack(side="top", fill="both", expand=True)
        self.configure(background="#0d0922")
        def findDir():
            saveDir = askdirectory()
            flist = os.listdir(saveDir)
            too = tk.Label(self, background="#0d0922")
            too.pack(side="top", fill="both", expand=True)
            lbox = tk.Listbox(self, highlightbackground="#0d0922", background="#0d0922", foreground="#d402d7")
            lbox.pack(side="left")
            for item in flist:
                if item.endswith('.json'):
                    lbox.insert(tk.END, item)
            def showcontent(event):
                x = lbox.curselection()
                file = lbox.get(x)
                p = saveDir+"/"+file
                with open(p, 'r', encoding='utf-8') as file:
                    file = file.read()
                    text.delete('1.0', tk.END)
                    text.insert(tk.END, file)
            def opensystem(event):
                x = lbox.curselection()[0]
                subprocess.call(["open", "-R", saveDir+"/"+lbox.get(x)])
                os.system(saveDir+"/"+lbox.get(x))
            text = tk.Text(self, fg='#ffe600', background='#0d0922', highlightbackground="#0d0922")
            text.pack(side="right")
            lbox.bind("<<ListboxSelect>>", showcontent)
            lbox.bind("<Double-Button-1>", opensystem)
        btnDir = tk.Button(self, text="Directory", highlightbackground="#0d0922", background="#0d0922", font=("Helvetica Neue", 16), command=findDir)
        btnDir.place(relx=0.4, rely=0)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        page1 = Page1(self)
        page2 = Page2(self)

        buttonframe = tk.Frame(self, background="#0d0922")
        container = tk.Frame(self, background="#0d0922")
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        page1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        page2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        button1 = tk.Button(buttonframe, text="Converter", highlightbackground="#0d0922", font=("Helvetica Neue", 16), command=page1.lift)
        button2 = tk.Button(buttonframe, text="Saves", highlightbackground="#0d0922", font=("Helvetica Neue", 16), command=page2.lift)
        button2.pack(side="right")
        button1.pack(side="right")

        page1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Profile Converter")
    root.minsize(550,300)
    root.maxsize(550,300)
    root.configure(background="#0d0922")
    root.mainloop()
