import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from typing import Union
from typing import Callable
import sqlite3
import domain
import webbrowser

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
mb = domain.Customer()

class FirstPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Movie Store Mangement system")

        self.button1 = ctk.CTkButton(self, text="Login as Membership", command=self.openLoginAsMember)

        self.button2 = ctk.CTkButton(self, text='Login as Admin' , command=self.openLoginAsAdmin)

        self.button3 = ctk.CTkButton(self, text="Sign Up", command=self.openSignUp)

        self.buttonQuit = ctk.CTkButton(master=self, text="Quit", command=self.destroy)

        self.button1.pack(side="top", padx=20, pady=20)
        self.button2.pack(side="top", padx=20, pady=20)
        self.button3.pack(side="top", padx=20, pady=20)
        self.buttonQuit.pack(side='top',padx=20,pady=20)

        self.LoginWindowAsMember = None
        self.LoginWindowAsAdmin = None
        self.SignUpWindow = None
    
    def openLoginAsMember(self):
        if self.LoginWindowAsMember is None or not self.LoginWindowAsMember.winfo_exists():
            self.LoginWindowAsMember = Membership(self)  # create window if its None or destroyed
        else:
            self.LoginWindowAsMember.focus()

    def openLoginAsAdmin(self):
        if self.LoginWindowAsAdmin is None or not self.LoginWindowAsAdmin.winfo_exists():
            self.LoginWindowAsAdmin = Admin(self)
        else:
            self.LoginWindowAsAdmin.focus()

    def openSignUp(self):
        if self.SignUpWindow is None or not self.SignUpWindow.winfo_exists():
            self.SignUpWindow = SignUp(self)  # create window if its None or destroyed
        else:
            self.SignUpWindow.focus()

class Admin(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = ctk.CTk()
        self.window.geometry("1000x400")
        self.window.title("Admin")

        self.frame = ctk.CTkFrame(master=self.window)
        # self.frame.pack(pady=20,padx=40,fill='both',expand=True)
        self.frame.pack(fill='both', expand='yes', padx=30, pady=20)

        label = ctk.CTkLabel(master=self.frame,text='Admin Login Window')
        label.pack(pady=12,padx=10)

        self.user_entry= ctk.CTkEntry(master=self.frame,placeholder_text="Admin Name")
        self.user_entry.pack(pady=12,padx=10)

        self.user_pass= ctk.CTkEntry(master=self.frame,placeholder_text="Password",show="*")
        self.user_pass.pack(pady=12,padx=10)


        button = ctk.CTkButton(master=self.frame,text='Login', command= self.login)
        button.pack(pady=12,padx=10)

        self.window.mainloop()

    def login(self):
        #One admin allowed
        username = 'admin'
        password = '1'

        if self.user_entry.get() != username or self.user_pass.get() != password:  
            tk.messagebox.showwarning(title='Warning',message='Login Failed')
        else:
            self.frame.destroy()

            #Initiate notebook
            self.notebook = ttk.Notebook(self.window)
            self.notebook.pack(pady=15)

            self.frame1 = tk.Frame(master=self.notebook, width=1000, height=600)
            self.frame2= tk.Frame(master=self.notebook, width=1000, height=600)

            self.frame1.pack(fill='both', expand=1)
            self.frame2.pack(fill='both', expand=1)

            self.notebook.add(self.frame1, text='Membership')
            self.notebook.add(self.frame2, text='Movie')

            self.createCustomerWidget()
            self.creatMovieWidget()

    def creatMovieWidget(self):
        self.frame3 = tk.Frame(master=self.frame2)
        self.frame3.pack(anchor='s')

        self.Table = ttk.Treeview(master=self.frame2, column=(1,2,3,4,5,6), show='headings', height='12')
        self.Table.pack()

        self.Table.column("#1",anchor=tk.CENTER, width=75)
        self.Table.column("#2",anchor=tk.CENTER, width=300)
        self.Table.column("#3",anchor=tk.CENTER, width=75)
        self.Table.column("#4",anchor=tk.CENTER, width=75)
        self.Table.column("#5",anchor=tk.CENTER, width=75)
        self.Table.column("#6",anchor=tk.CENTER, width=300)
        
        self.Table.heading(1, text='Id')
        self.Table.heading(2, text='Title')
        self.Table.heading(3, text='Duration')
        self.Table.heading(4, text='Cost')
        self.Table.heading(5, text='Quantity')
        self.Table.heading(6, text='Link')

        self.Table.bind('<Double 1>', self.getrow)

        self.conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Movie_Data 
                                (Id INTEGER PRIMARY KEY, Title TEXT, Duration TEXT, Cost TEXT, Quantity INT, Link TEXT)
                        '''
        self.cur = self.conn.cursor()
        self.conn.execute(table_create_query)
        self.conn.commit()

        self.update()

        self.t1 = tk.StringVar()
        self.t2 = tk.StringVar()
        self.t3 = tk.StringVar()
        self.t4 = tk.StringVar()
        self.t5 = tk.IntVar()
        self.t6 = tk.StringVar()

        self.lbl1 = tk.Label(self.frame3,text='Movie ID')
        self.lbl1.grid(row=0, column=0,padx=20,pady=5)
        self.ent1 = tk.Entry(self.frame3, textvariable=self.t1)
        self.ent1.grid(row=0, column=1, padx=5, pady=3)

        self.lbl2 = tk.Label(self.frame3,text='Title')
        self.lbl2.grid(row=0, column=2, padx=5, pady=3)
        self.ent2 = tk.Entry(self.frame3, textvariable=self.t2)
        self.ent2.grid(row=0, column=3, padx=5, pady=3)

        self.lbl3 = tk.Label(self.frame3,text='Duration')
        self.lbl3.grid(row=1, column=0, padx=5, pady=3)
        self.ent3 = tk.Entry(self.frame3, textvariable=self.t3)
        self.ent3.grid(row=1, column=1, padx=5, pady=3)

        self.lbl4 = tk.Label(self.frame3,text='Cost')
        self.lbl4.grid(row=1, column=2, padx=5, pady=3)
        self.ent4 = tk.Entry(self.frame3, textvariable=self.t4)
        self.ent4.grid(row=1, column=3, padx=5, pady=3)

        self.lbl5 = tk.Label(self.frame3,text='Quantity')
        self.lbl5.grid(row=2, column=0, padx=5, pady=3)
        self.ent5 = tk.Entry(self.frame3, textvariable=self.t5)
        self.ent5.grid(row=2, column=1, padx=5, pady=3)

        self.lbl6 = tk.Label(self.frame3,text='Link')
        self.lbl6.grid(row=2, column=2, padx=5, pady=3)
        self.ent6 = tk.Entry(self.frame3, textvariable=self.t6)
        self.ent6.grid(row=2, column=3, padx=5, pady=3)

        upbut = tk.Button(self.frame3, text='Update', command=self.updateMovie)
        addbut = tk.Button(self.frame3, text = 'Add New', command=self.addMovie)
        delbut = tk.Button(self.frame3, text = 'Delete', command=self.delMovie)
        clsbut = tk.Button(self.frame3, text = 'Clear', command=self.clear_entries)

        upbut.grid(row=4, column=0, padx=5, pady=3)
        addbut.grid(row=4, column=1, padx=5, pady=3)
        delbut.grid(row=4, column=2, padx=5, pady=3)
        clsbut.grid(row=4, column=3, padx=5, pady=3)


    def clearTree(self):
        self.Table.delete(*self.Table.get_children())

    def update(self):
        self.clearTree()
        self.cur.execute("SELECT * FROM Movie_Data")
        rows = self.cur.fetchall()
        for i in rows:
            self.Table.insert('','end',values=i)

    def getrow(self,event):
        self.clear_entries()
        selected = self.Table.selection()[0]
        self.ent1.insert(0, self.Table.item(selected)['values'][0])
        self.ent2.insert(0, self.Table.item(selected)['values'][1])
        self.ent3.insert(0, self.Table.item(selected)['values'][2])
        self.ent4.insert(0, self.Table.item(selected)['values'][3])
        self.ent5.insert(0, self.Table.item(selected)['values'][4])
        self.ent6.insert(0, self.Table.item(selected)['values'][5])

        

    def updateMovie(self):
        id = self.ent1.get()
        title = self.ent2.get()
        duration = self.ent3.get()
        cost = self.ent4.get()
        quantity = self.ent5.get()
        link = self.ent6.get()
        query = "UPDATE Movie_Data SET Title = ? , Duration = ?, Cost = ? , Quantity = ?,Link = ? WHERE Id = ?"
        data_insert_tuple = (title, duration, cost, quantity, link, id)
        self.conn.execute(query, data_insert_tuple)
        self.conn.commit()
        self.update()

    def addMovie(self):
        title = self.ent2.get()
        duration = self.ent3.get()
        cost = self.ent4.get()
        quantity = self.ent5.get()
        link = self.ent6.get()
        query = "INSERT INTO Movie_Data(Id , Title , Duration, Cost , Quantity,Link) VALUES(NULL,?,?,?,?,?)"
        data_insert_tuple = (title, duration, cost, quantity, link)
        self.conn.execute(query, data_insert_tuple)
        self.conn.commit()
        self.update()

    def delMovie(self):
        id = self.ent1.get()
        query = 'DELETE FROM Movie_Data WHERE Id  ='+id
        self.conn.execute(query)
        self.conn.commit()
        self.update()
    
    def clear_entries(self):
        self.ent1.delete(0, 'end')
        self.ent2.delete(0, 'end')
        self.ent3.delete(0, 'end')
        self.ent4.delete(0, 'end')
        self.ent5.delete(0, 'end')
        self.ent6.delete(0, 'end')
            

    def createCustomerWidget(self):
        #Customer mangment
        #First Name
        self.FirstNameLabel = tk.Label(self.frame1, text="First Name:",font=('Roboto',14))
        self.FirstNameLabel.grid(row=0, column=0,padx=20,pady=5)
        self.FirstNameEntry = tk.Entry(self.frame1)
        self.FirstNameEntry.grid(row=0, column=1,padx=20,pady=5)

        #Last Name
        self.LastNameLabel = tk.Label(self.frame1, text='Last Name:',font=('Roboto',14))
        self.LastNameLabel.grid(row=0, column=2,padx=20,pady=5)
        self.LastNameEntry = tk.Entry(self.frame1)
        self.LastNameEntry.grid(row=0, column=3,padx=20,pady=5)

        #Date of birth
        self.DoBLabel = tk.Label(self.frame1, text='Date of birth:',font=('Roboto',14))
        self.DoBLabel.grid(row=1, column=0,padx=20,pady=5)
        self.DoBEntry = tk.Entry(self.frame1)
        self.DoBEntry.grid(row=1, column=1,padx=20,pady=5)

        #Gender
        self.GenderLabel = tk.Label(self.frame1, text='Gender:',font=('Roboto',14))
        self.GenderLabel.grid(row=2, column=0,padx=20,pady=5)
        self.GenderComboBox = tk.Entry(self.frame1)
        self.GenderComboBox.grid(row=2, column=1,padx=20,pady=5)

        #Age
        self.AgeLabel = tk.Label(self.frame1, text='Age:',font=('Roboto',14))
        self.AgeLabel.grid(row=2, column=2,padx=20,pady=5)
        self.AgeEntry = tk.Entry(self.frame1)
        self.AgeEntry.grid(row=2, column=3,padx=20,pady=5)

        #Address
        self.AddressLabel = tk.Label(self.frame1, text='Address:',font=('Roboto',14))
        self.AddressLabel.grid(row=3, column=0,padx=20,pady=5)
        self.AddressEntry = tk.Entry(self.frame1, width=50)
        self.AddressEntry.grid(row=3, column=1,padx=20,pady=5, columnspan=2)

        #Phone
        self.PhoneLable = tk.Label(self.frame1, text='Phone:',font=('Roboto',14))
        self.PhoneLable.grid(row=4, column=0,padx=20,pady=5)
        self.PhoneEntry = tk.Entry(self.frame1)
        self.PhoneEntry.grid(row=4, column=1,padx=20,pady=5)

        #User
        self.UserLabel = tk.Label(self.frame1, text='User name:',font=('Roboto',14))
        self.UserLabel.grid(row=5, column=0,padx=20,pady=5)
        self.UserEntry = tk.Entry(self.frame1)
        self.UserEntry.grid(row=5, column=1,padx=20,pady=5)

        #Password
        self.PasswordLabel = tk.Label(self.frame1, text='Password:',font=('Roboto',14))
        self.PasswordLabel.grid(row=5, column=2,padx=20,pady=5)
        self.PassEntry = tk.Entry(self.frame1)
        self.PassEntry.grid(row=5, column=3,padx=20,pady=5)

        # Parts list (listbox)
        self.MemberList = tk.Listbox(master=self.frame1, height=20, width=35, border=0)
        self.MemberList.grid(row=0, column=4, columnspan=10,
                                rowspan=10, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar1 = tk.Scrollbar(master=self.frame1)
        self.scrollbar1.grid(row=0, column=15)

        # Set scrollbar to parts
        self.MemberList.configure(yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.configure(command=self.MemberList.yview)

        # Bind select
        self.MemberList.bind('<<ListboxSelect>>', self.Select)

        # Buttons
        self.AddButton = tk.Button(
                master=self.frame1, text="Add Member", width=12, command=self.Add)
        self.AddButton.grid(row=6, column=0, pady=20)

        self.RemoveButton = tk.Button(
                master=self.frame1, text="Remove Member", width=12, command=self.Remove)
        self.RemoveButton.grid(row=6, column=1)

        self.UpdateButton = tk.Button(
                master=self.frame1, text="Update Info", width=12, command=self.Update)
        self.UpdateButton.grid(row=6, column=2)

        self.ClearButton = tk.Button(
                master=self.frame1, text="Clear Input", width=12, command=self.Clear)
        self.ClearButton.grid(row=6, column=3)

        self.selected_index = 0
        self.Refresh()
    
    def Refresh(self):
        # Delete value before update
        self.MemberList.delete(0, tk.END)
        # Loop through records
        for row in mb.fetch():
            # Insert into list
            self.MemberList.insert(tk.END, row)

    # Add new mem
    def Add(self):
        if self.FirstNameEntry.get() == '' or self.LastNameEntry.get() == '' or self.GenderComboBox.get() == '' or self.AgeEntry.get() == ''\
            or self.DoBEntry.get() == '' or self.AddressEntry.get() == '' or self.PhoneEntry.get() == '' or self.UserEntry.get() == ''\
            or self.PassEntry.get() == '' :
            tk.messagebox.showerror("Required Fields", "Please include all fields")

        # Insert into DB
        mb.insert(self.FirstNameEntry.get(), self.LastNameEntry.get(), self.DoBEntry.get(), self.AgeEntry.get(), self.GenderComboBox.get()\
            , self.AddressEntry.get(), self.PhoneEntry.get(), self.UserEntry.get()\
            , self.PassEntry.get())
        
        # Clear list
        self.MemberList.delete(0, tk.END)
        # Insert into list
        self.MemberList.insert(tk.END, self.FirstNameEntry.get(), self.LastNameEntry.get(), self.DoBEntry.get(), self.GenderComboBox.get(), self.AgeEntry.get()\
            , self.AddressEntry.get(), self.PhoneEntry.get(), self.UserEntry.get()\
            , self.PassEntry.get())
        
        self.Clear()
        self.Refresh()

    # Runs when value is selected
    def Select(self, event):
        try:
            # Get index
            index = self.MemberList.curselection()[0]
            # Get selected value
            self.selected_index = self.MemberList.get(index)

            # Add text to entries
            self.FirstNameEntry.delete(0, tk.END)
            self.FirstNameEntry.insert(tk.END, self.selected_index[1])
            self.LastNameEntry.delete(0, tk.END)
            self.LastNameEntry.insert(tk.END, self.selected_index[2])
            self.DoBEntry.delete(0, tk.END)
            self.DoBEntry.insert(tk.END, self.selected_index[3])
            self.AgeEntry.delete(0, tk.END)
            self.AgeEntry.insert(tk.END, self.selected_index[4])
            self.GenderComboBox.delete(0, tk.END)
            self.GenderComboBox.insert(tk.END, self.selected_index[5])
            self.AddressEntry.delete(0, tk.END)
            self.AddressEntry.insert(tk.END, self.selected_index[6])
            self.PhoneEntry.delete(0, tk.END)
            self.PhoneEntry.insert(tk.END, self.selected_index[7])
            self.UserEntry.delete(0, tk.END)
            self.UserEntry.insert(tk.END, self.selected_index[8])
            self.PassEntry.delete(0, tk.END)
            self.PassEntry.insert(tk.END, self.selected_index[9])
        except IndexError:
            pass

    # Remove member
    def Remove(self):
        mb.remove(self.selected_index[0])
        self.Clear()
        self.Refresh()

    # Update member info
    def Update(self):
        mb.update(self.selected_index[0], self.FirstNameEntry.get(), self.LastNameEntry.get(), self.DoBEntry.get(), self.GenderComboBox.get(), self.AgeEntry.get()\
            , self.AddressEntry.get(), self.PhoneEntry.get(), self.UserEntry.get(), self.PassEntry.get())
        self.Refresh()

    # Clear all text fields
    def Clear(self):
        self.FirstNameEntry.delete(0, tk.END)
        self.LastNameEntry.delete(0, tk.END)
        self.GenderComboBox.delete(0, tk.END)
        self.DoBEntry.delete(0, tk.END)
        self.GenderComboBox.delete(0, tk.END)
        self.AgeEntry.delete(0, tk.END)
        self.AddressEntry.delete(0, tk.END)
        self.PhoneEntry.delete(0, tk.END)
        self.UserEntry.delete(0, tk.END)
        self.PassEntry.delete(0, tk.END)


class Membership(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = ctk.CTk()
        self.window.geometry("700x400")
        self.window.title("Membership")

        self.frame = ctk.CTkFrame(master=self.window)
        self.frame.pack(pady=20,padx=40,fill='both',expand=True)

        label = ctk.CTkLabel(master=self.frame,text='Customer Login Screen')
        label.pack(pady=12,padx=10)


        self.user_entry= ctk.CTkEntry(master=self.frame,placeholder_text="Username")
        self.user_entry.pack(pady=12,padx=10)

        self.user_pass= ctk.CTkEntry(master=self.frame,placeholder_text="Password",show="*")
        self.user_pass.pack(pady=12,padx=10)


        button = ctk.CTkButton(master=self.frame,text='Login', command= self.login)
        button.pack(pady=12,padx=10)

        checkbox = ctk.CTkCheckBox(master=self.frame,text='Remember Me')
        checkbox.pack(pady=12,padx=10)

        self.window.mainloop()

    def login(self):
        username = self.user_entry.get()
        password = self.user_pass.get()

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        statement = f"SELECT UserName from Client_Data WHERE username='{username}' AND Password = '{password}';"
        cur.execute(statement)
        if not cur.fetchone():  
            tk.messagebox.showwarning(title='Warning',message='Login Failed')
        else:
            self.frame.destroy()
            self.createMemberWidget()
    
    def createMemberWidget(self):
        self.frame1 = ctk.CTkFrame(master=self.window)
        self.frame1.pack(pady=20,padx=40,fill='both',expand=True)

        self.frame2 = ctk.CTkFrame(master=self.window)
        self.frame2.pack(pady=20,padx=40,fill='both',expand=True)

        self.Table = ttk.Treeview(master=self.frame1, column=(1,2,3,4,5,6), show='headings', height='12')
        self.Table.pack()

        self.Table.column("#1",anchor=tk.CENTER, width=75)
        self.Table.column("#2",anchor=tk.CENTER, width=300)
        self.Table.column("#3",anchor=tk.CENTER, width=150)
        self.Table.column("#4",anchor=tk.CENTER, width=125)
        self.Table.column("#5",anchor=tk.CENTER, width=125)

        self.Table.heading(1, text='Id')
        self.Table.heading(2, text='Title')
        self.Table.heading(3, text='Duration')
        self.Table.heading(4, text='Cost')
        self.Table.heading(5, text='Quantity')

        self.Table.bind('<Double 1>', self.getrow)

        self.conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Movie_Data 
                                (Id INTEGER PRIMARY KEY, Title TEXT, Duration TEXT, Cost TEXT, Quantity INT, Link TEXT)
                        '''
        self.cur = self.conn.cursor()
        self.conn.execute(table_create_query)
        self.conn.commit()

        self.update()

        # These entries are fake
        self.ent = ctk.CTkEntry(self.frame2)
        self.ent1 = ctk.CTkEntry(self.frame2)

        # This entry is real
        self.ent2 = ctk.CTkEntry(self.frame2)

        self.BuyButton = ctk.CTkButton(
                master=self.frame2, text="Buy", width=50, fg_color='green', command=self.BuyMovie)
        self.BuyButton.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    def BuyMovie(self):
        try:
            quantity = self.ent.get()
            id = self.ent1.get()
            link = self.ent2.get()
            realQuantity = int(quantity)
            if realQuantity == 1:
                query = 'DELETE FROM Movie_Data WHERE Id  ='+id
                self.conn.execute(query)
            else:
                query = 'UPDATE Movie_Data SET Quantity = Quantity - 1 WHERE Id = ?'
                self.conn.execute(query,id)
            self.update()
            self.conn.commit()

            self.watchButton = ctk.CTkButton(master=self.frame2, text="Watch Now", width=50, fg_color='green', command=self.OpenMovie)
            self.watchButton.grid(row=2, column=0, sticky="news", padx=20, pady=10)
            self.ent2.grid(row=2, column=1, sticky="news", padx=20, pady=10)
            
        except:
            tk.messagebox.showwarning(title='Warning',message='Pick a fukin movie')

    def OpenMovie(self):
        link = self.ent2.get()
        webbrowser.open(link, new = 2)

    def clearTree(self):
        self.Table.delete(*self.Table.get_children())

    def update(self):
        self.clearTree()
        self.cur.execute("SELECT Id, Title, Duration, Cost, Quantity, Link FROM Movie_Data")
        rows = self.cur.fetchall()
        for i in rows:
            self.Table.insert('','end',values=i)

    def clear_entries(self):
        self.ent.delete(0, 'end')
        self.ent1.delete(0,'end')
        self.ent2.delete(0,'end')
    
    def getrow(self,event):
        self.clear_entries()
        selected = self.Table.selection()[0]
        self.ent1.insert(0, self.Table.item(selected)['values'][0])
        self.ent.insert(0, self.Table.item(selected)['values'][4])
        self.ent2.insert(0, self.Table.item(selected)['values'][5])


class SignUp(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = ctk.CTk()
        self.window.title("Data Entry Form")

        frame = ctk.CTkFrame(self.window)
        frame.pack()

        #Title frame
        self.frame1 = ctk.CTkFrame(frame)
        self.frame1.grid(row=0, column=0, padx=10, pady=0)
        TitleLabel = ctk.CTkLabel(self.frame1,text='Sign up form',font=('Roboto',42,'bold'))
        TitleLabel.grid(padx=0,pady=0)

        #User information frame
        self.frame =ctk.CTkFrame(frame)
        self.frame.grid(row=2, column=0, padx=20, pady=10)

        #Define labels
        TitleLabel1 = ctk.CTkLabel(self.frame, text='User Info',font=('Roboto',18,'bold'))
        FirstNameLabel = ctk.CTkLabel(self.frame, text="First Name:",font=('Roboto',14))    #Entry Str
        LastNameLabel = ctk.CTkLabel(self.frame, text='Last Name:',font=('Roboto',14))      #Entry Str
        DoBLabel = ctk.CTkLabel(self.frame, text='Date of birth:',font=('Roboto',14))       #Entry Str / might try tkcalendar
        GenderLabel = ctk.CTkLabel(self.frame, text='Gender:',font=('Roboto',14))           #ComboBox Str
        AgeLabel = ctk.CTkLabel(self.frame, text='Age:',font=('Roboto',14))                 #IntSpinbox Int
        AddressLabel = ctk.CTkLabel(self.frame, text='Address:',font=('Roboto',14))         #Entry Str
        PhoneLable = ctk.CTkLabel(self.frame, text='Phone:',font=('Roboto',14))             #Entry Str

        #Define entries
        self.FirstNameEntry = ctk.CTkEntry(self.frame,placeholder_text='Emanuel')
        self.LastNameEntry = ctk.CTkEntry(self.frame,placeholder_text='Macron')
        self.DoBEntry = ctk.CTkEntry(self.frame,placeholder_text='21/12/1977')
        self.GenderComboBox = ctk.CTkOptionMenu(self.frame,width=150,height=30, values=['Male', 'Female', '??Gay??'])
        self.AgeSpinBox = Spinbox(self.frame, step_size=1)
        self.AgeSpinBox.set(18)      #No spinbox in custom tkinter so I make one
        self.AddressEntry = ctk.CTkEntry(self.frame,width=400,height=30,placeholder_text='33 avenue Jean Portalis, Tours')
        self.PhoneEntry = ctk.CTkEntry(self.frame,width=200,height=30,placeholder_text='02.64.68.86.15')
        
        #Arrange User Infomation
        TitleLabel1.grid(row=0, column=0,padx=20,pady=5, sticky='W')
        FirstNameLabel.grid(row=2, column=0, padx=10,pady=20)
        self.FirstNameEntry.grid(row=2, column=1, padx=20,pady=20)
        LastNameLabel.grid(row=2, column=2, padx=10,pady=20)
        self.LastNameEntry.grid(row=2, column=3, padx=20,pady=20)
        DoBLabel.grid(row=3,column=0, padx=10,pady=20)
        self.DoBEntry.grid(row=3,column=1, padx=20, pady=20)
        AgeLabel.grid(row=3,column=2, padx=10,pady=20)
        self.AgeSpinBox.grid(row=3,column=3, padx=20,pady=20)
        GenderLabel.grid(row=4,column=0, padx=10,pady=20)
        self.GenderComboBox.grid(row=4,column=1, padx=20,pady=20)
        AddressLabel.grid(row=5,column=0,padx=10,pady=20)
        self.AddressEntry.grid(row=5,column=1,padx=20,pady=20, columnspan=4)
        PhoneLable.grid(row=6,column=0,padx=10,pady=20)
        self.PhoneEntry.grid(row=6,column=1,padx=20,pady=20, columnspan=2)

        #SignUp account frame
        self.frame2 = ctk.CTkFrame(frame)
        self.frame2.grid(row=6, column=0, sticky="news", padx=20, pady=10)
        TitleLabel2 = ctk.CTkLabel(self.frame2, text='Account Register',font=('Roboto',18,'bold'))

        #Label
        UserLabel = ctk.CTkLabel(self.frame2, text='User name:',font=('Roboto',14))             #Entry Str
        PasswordLabel = ctk.CTkLabel(self.frame2, text='Password for new account:',font=('Roboto',14))   #Entry Str
        PasswordCondition = ctk.CTkLabel(self.frame2, text='*Password must contain atleast 6 character', font=('Roboto',10)) #under password entry

        #Entries
        self.UserEntry = ctk.CTkEntry(self.frame2,placeholder_text='ProbalyNotMacron')
        self.PasswordEntry = ctk.CTkEntry(self.frame2,placeholder_text='Vive la France')

        #Arrangement of frame2
        TitleLabel2.grid(row=0, column=0,padx=20,pady=5, sticky='W')
        UserLabel.grid(row=2, column=0, padx=10,pady=10)
        self.UserEntry.grid(row=2, column=1, padx=20,pady=10)
        PasswordLabel.grid(row=3, column=0, padx=10,pady=10)
        self.PasswordEntry.grid(row=3, column=1, padx=20,pady=10)

        # Terms frame
        self.frame3 = ctk.CTkLabel(frame, text="Terms & Conditions")
        self.frame3.grid(row=8, column=0, sticky="news", padx=20, pady=10)

        self.AcceptVar = ctk.StringVar(value="Not Accepted")
        TermCheck = ctk.CTkCheckBox(self.frame3, text= "I accept the terms and conditions.",
                                        variable=self.AcceptVar, onvalue="Accepted", offvalue="Not Accepted")
        TermCheck.grid(row=0, column=0)

        #Powerfull button
        RegisterButton = ctk.CTkButton(self.frame3, text="Sign Up", fg_color='green', command=self.EnterData)
        RegisterButton.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        self.window.mainloop()

    def EnterData(self):
        accepted = self.AcceptVar.get()
        
        if accepted=="Accepted":
            # User info
            FirstName = self.FirstNameEntry.get()
            LastName = self.LastNameEntry.get()
            
            if FirstName and LastName:
                DoB = self.DoBEntry.get()
                Age = self.AgeSpinBox.get()
                Gender = self.GenderComboBox.get()
                Address = self.AddressEntry.get()
                Phone = self.PhoneEntry.get()
                
                User = self.UserEntry.get()
                Password = self.PasswordEntry.get()
                
                # Create Table
                conn = sqlite3.connect('data.db')
                table_create_query = '''CREATE TABLE IF NOT EXISTS Client_Data 
                        (Id INTEGER PRIMARY KEY, Firstname TEXT, Lastname TEXT, DateOfBirth TEXT, Age INT, Gender TEXT, 
                        Address TEXT, PhoneNumber TEXT, UserName TEXT, Password TEXT)
                '''
                conn.execute(table_create_query)
                
                # Insert Data
                data_insert_query = '''INSERT INTO Client_Data (Id, Firstname, Lastname, DateOfBirth, 
                Age, Gender, Address, PhoneNumber, UserName, Password) VALUES 
                (NULL,?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                data_insert_tuple = (FirstName, LastName, DoB,
                                    Age, Gender, Address, Phone, User, Password)
                cursor = conn.cursor()
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()
                print('Register sucessful')
                self.window.destroy()      
            else:
                tk.messagebox.showwarning(title="Error", message="First name and last name are required.")
        else:
            tk.messagebox.showwarning(title= "Error", message="You have not accepted the terms")

class Spinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int =100,
                 step_size: Union[int, int] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.subtract_button = ctk.CTkButton(self, text="-", width=25, height=10,
                                             anchor=tk.CENTER,
                                            command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=3)

        self.entry = ctk.CTkEntry(self, width=100, height=30, border_width=0)
        self.entry.grid(row=0, column=0, rowspan = 2)

        self.add_button = ctk.CTkButton(self, text="+", width=25, height=10,
                                        anchor=tk.CENTER,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2)

        # default value
        self.entry.insert(0, "0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

    

if __name__ == "__main__":
    run = FirstPage()
    run.mainloop()