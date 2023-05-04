import tkinter as tk
from tkinter import messagebox
import sqlite3
import string
import random
import pyperclip
from twilio.rest import Client

conn = sqlite3.connect("test1.db")
cursor = conn.cursor()
main = "Password Manager/"

account_sid = '#################################' #enter your twilio account_sid
auth_token = '#################################'  #enter your twilio auth_token
client = Client(account_sid, auth_token)


class Login:
    def __init__(self, master):
        self.master = master
        self.master.title(main + "Login Page")
        self.master.geometry("250x100")
        self.master.configure(bg='#32538c')
        self.username = tk.Label(self.master, text="Username")
        self.passwd = tk.Label(self.master, text="Password")
        self.e_username = tk.Entry(self.master, width=20)
        # username placeholder
        self.e_username.insert(0, "Username")
        self.e_username.config(fg='gray')
        self.e_passwd = tk.Entry(self.master, width=20)
        # Introducing the place-hOlder Effect
        self.e_passwd.insert(0, "Enter Master Password")
        # setting the initial color of the text in the entry to gray
        self.e_passwd.config(fg='gray')
        self.login = tk.Button(self.master, text="Login", command=self.logon)
        self.username.grid(row=0, column=0)
        self.passwd.grid(row=1, column=0)
        self.e_username.grid(row=0, column=1)
        self.e_passwd.grid(row=1, column=1)
        self.login.grid(row=2, column=1)
        # move next to the next entry widget when Return/Enter Key
        # is pressed
        self.e_username.bind('<Return>', self.move_next)
        self.e_passwd.bind('<Return>', self.move_next)
        # bind the on_click_entry function to the FocusIn event
        # clears the entry widget
        self.e_username.bind('<FocusIn>', self.on_click_entry)
        self.e_passwd.bind('<FocusIn>', self.on_click_entry)

    # define a function that clears the entry text
    def on_click_entry(self, event):
        if self.e_username.get() == "Username":
            self.e_username.delete(0, tk.END)
            self.e_username.config(fg='black')
        elif self.e_passwd.get() == "Enter Master Password":
            self.e_passwd.delete(0, tk.END)
            self.e_passwd.config(fg='black', show='*')

    def move_next(self, event):
        event.widget.tk_focusNext().focus()

    def logon(self):
        uname = self.e_username.get()
        passw = self.e_passwd.get()

        if uname == "a" and passw == "a":
            self.master.withdraw()
            home = tk.Toplevel(self.master)
            Home(home)
        else:
            messagebox.showwarning('Wrong Credentials', message="Invalid Username or Password!")


# Homepage window class


class Home:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x300')
        self.master.configure(bg='#32538c')
        self.master.title(main + "Home Page")
        self.sitename = tk.Label(self.master, text="SiteName/URL")
        self.username = tk.Label(self.master, text="Username")
        self.passwd = tk.Label(self.master, text="Password")
        self.desc = tk.Label(self.master, text="Description")
        self.close_btn = tk.Button(self.master, text="Exit", command=self.destroy_all)
        self.e_sitename = tk.Entry(self.master, width=20)
        self.e_username = tk.Entry(self.master, width=20)
        self.e_passwd = tk.Entry(self.master, width=20, show='*')
        self.e_desc = tk.Entry(self.master, width=20)
        self.move_btn = tk.Button(self.master, text="Display", bg="green", command=self.display)
        self.clear_btn = tk.Button(self.master, text='Clear', bg='green', command=self.clear)
        self.save_btn = tk.Button(self.master, text="Save", command=self.save_to_db)
        self.generate_btn = tk.Button(self.master, text="Generate Password", bg="orange", command=self.generate)
        self.delete_btn = tk.Button(self.master, text="Delete User", command=self.delete_entry)
        self.sitename.grid(row=0, column=0)
        self.username.grid(row=1, column=0)
        self.passwd.grid(row=2, column=0)
        self.desc.grid(row=3, column=0)
        self.e_sitename.grid(row=0, column=1)
        self.e_username.grid(row=1, column=1)
        self.e_passwd.grid(row=2, column=1)
        self.e_desc.grid(row=3, column=1)
        self.move_btn.grid(row=4, column=1)
        self.clear_btn.grid(row=4, column=0)
        self.delete_btn.grid(row=5, column=0)
        self.save_btn.grid(row=5, column=1)
        self.generate_btn.grid(row=6, column=1)
        self.close_btn.grid(row=7, column=1)
        # save to db elements
        self.website = self.e_sitename.get()
        self.uname = self.e_username.get()
        self.pass_wd = self.e_passwd.get()
        self.describe = self.e_desc.get()

    # Define function to save the contents of the entry widget to the
    # database

    def save_to_db(self):
        self.website = self.e_sitename.get()
        self.uname = self.e_username.get()
        self.pass_wd = self.e_passwd.get()
        self.describe = self.e_desc.get()

        # cursor.execute("INSERT INTO user(username) VALUES(?)", (self.uname,))

        # print(self.uname)

        # Check the Length of the Password entered

        if len(self.pass_wd) < 8:
            messagebox.showinfo(message="Password is too short")


        else:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user(ID INTEGER PRIMARY KEY AUTOINCREMENT, website text, username text,Passwd text, description text)")

            cursor.execute("INSERT INTO user(website,username,Passwd, description) VALUES(?,?,?,?)",
                           (self.website, self.uname, self.pass_wd, self.describe))

            conn.commit()

            messagebox.showinfo(message="Saved Successfully")


    def delete_entry(self):
        self.user = self.e_username.get()
        cursor.execute("SELECT * FROM user WHERE website = ?", (self.user,))
        web = cursor.fetchone()
        # check if the user exists in the db and delete em if they exist
        if web is not None:
            messagebox.showinfo(message="user does not exist")


        else:
            cursor.execute("DELETE FROM user WHERE username=?", (self.user,))
            conn.commit()
            messagebox.showinfo(message="Account Credentials Deleted Successfully!")

    def clear(self):
        self.e_sitename.delete(0, tk.END)
        self.e_username.delete(0, tk.END)
        self.e_passwd.delete(0, tk.END)
        self.e_desc.delete("1.0", tk.END)

    # Function to move to display window

    def display(self):
        self.master.withdraw()
        display = tk.Toplevel(self.master)
        Display(display)

    # Function to move to Generate window
    def generate(self):
        self.master.withdraw()
        generate = tk.Toplevel(self.master)
        Generate(generate)

    def destroy_all(self):
        # destroy all widgets
        for widget in root.winfo_children():
            widget.destroy()
        # destroy root window
        root.destroy()


# Create a class for Display Window
class Display:
    def __init__(self, master):
        self.usernm = None
        self.master = master
        self.master.configure(bg='#32538c')
        self.master.title(main + "Display Window")
        self.master.geometry('400x300')
        self.home = Home
        self.website = tk.Entry(self.master, width=34)
        self.label = tk.Label(self.master, text="Enter the Site URL", width=34)
        self.back_btn = tk.Button(self.master, text="Back", bg="red", command=self.back)
        self.display_btn = tk.Button(self.master, text="Display Contents", command=self.display_db)
        self.close_btn = tk.Button(self.master, text="Exit", command=self.destroy_all)
        self.clear_btn = tk.Button(self.master, text="Clear", command=self.clear)
        self.disp_text = tk.Text(self.master, width=40, height=7)
        self.label.pack()
        self.website.pack()
        self.back_btn.pack()

        self.display_btn.pack()
        self.close_btn.pack()
        self.clear_btn.pack()
        self.disp_text.pack()
        self.usern = self.website.get()

        self.website.bind('<FocusIn>', self.on_click_entry)

    def clear(self):
        self.website.delete(0, tk.END)

    def on_click_entry(self, event):
        if self.website.get() == "Username":
            self.website.delete(0, tk.END)
            self.website.config(fg='black')

    def display_db(self):
        self.usern = self.website.get()

        cursor.execute('SELECT Passwd FROM user WHERE website = ?', (self.usern,))
        passwd = cursor.fetchone()
        cursor.execute('SELECT username FROM user WHERE website = ?', (self.usern,))
        web = cursor.fetchone()
        cursor.execute('SELECT description FROM user WHERE website = ?', (self.usern,))
        aoi = cursor.fetchone()

        # convert the tuples to strings
        passtring = ''.join(map(str, passwd))
        webstring = ''.join(map(str, web))
        description = ''.join(map(str, aoi))

        message = client.messages.create(
            from_='##########',
            body="UserNAme:" + webstring + "\n" "Password:" + passtring + "\n" "Account Info:" + description,
            to='##########'    # registered twilio number
        )

        print(message.sid)
        messagebox.showinfo(message="Credentials Sent Successfully! Check Your Phone")

        # print(self.usernm)


    def back(self):
        self.master.withdraw()
        home = tk.Toplevel(self.master)
        Home(home)

    def destroy_all(self):
        self.home.destroy_all(self)


class Generate:
    def __init__(self, master):
        self.master = master
        self.master.geometry('400x300')
        self.master.configure(bg='#32538c')
        self.master.title(main + "Generator")
        # create an instance of Class "Home"
        # To use functions defined in Home
        self.savedb = Home
        self.sitename = tk.Label(self.master, text="SiteName/URL")
        self.username = tk.Label(self.master, text="Username")
        self.passwd = tk.Label(self.master, text="Password")
        self.desc = tk.Label(self.master, text="Description")
        self.close_btn = tk.Button(self.master, text="Exit", command=self.destroy_all)
        self.home = tk.Button(self.master, text="Home", command=self.home)
        self.e_sitename = tk.Entry(self.master, width=20)
        self.e_username = tk.Entry(self.master, width=20)
        self.e_passwd = tk.Entry(self.master, width=20, show='*')
        self.e_desc = tk.Entry(self.master, width=20)
        self.move_btn = tk.Button(self.master, text="Display", bg="green", command=self.display)
        self.clear_btn = tk.Button(self.master, text='Clear', bg='green', command=self.Clear)
        self.save_btn = tk.Button(self.master, text="Save", command=self.save_to_db)
        self.gen_btn = tk.Button(self.master, text="Generate", command=self.generator)
        self.delete_btn = tk.Button(self.master, text="Delete User", command=self.delete_entry)
        self.sitename.grid(row=0, column=0)
        self.username.grid(row=1, column=0)
        self.passwd.grid(row=2, column=0)
        self.desc.grid(row=3, column=0)
        self.e_sitename.grid(row=0, column=1)
        self.e_username.grid(row=1, column=1)
        self.e_passwd.grid(row=2, column=1)
        self.e_desc.grid(row=3, column=1)
        self.clear_btn.grid(row=4, column=0)
        self.move_btn.grid(row=4, column=1)
        self.save_btn.grid(row=5, column=1)
        self.delete_btn.grid(row=5, column=2)
        self.gen_btn.grid(row=5, column=0)
        self.close_btn.grid(row=6, column=1)
        self.home.grid(row=6, column=0)
        # function generator instances
        self.rad = string.ascii_letters + string.digits + string.punctuation
        self.password = random.choice(string.punctuation)
        self.password += random.choice(string.ascii_uppercase)
        self.password += random.choice(string.hexdigits)
        self.password += random.choice(string.ascii_lowercase)

    def delete_entry(self):
        self.savedb.delete_entry(self)

    # Destroy All classes
    def destroy_all(self):
        self.savedb.destroy_all(self)

    # call function save_to_db from class Home
    def save_to_db(self):
        self.savedb.save_to_db(self)

    def Clear(self):
        self.savedb.clear(self)

    def display(self):
        self.master.withdraw()
        display = tk.Toplevel(self.master)
        Display(display)

    def home(self):
        self.master.withdraw()
        home = tk.Toplevel(self.master)
        Home(home)


    # Create a function to copy to the clipboard
    # text that has been generated
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def generator(self):
        for i in range(8):
            self.password += random.choice(self.rad)

        # self.password_l = tk.Label(self.master, textvariable=self.password, font=25)
        # self.password_l.pack()
        self.copy_to_clipboard(self.password)
        messagebox.showinfo(self.master, message=self.password)
        self.e_passwd.delete(0, tk.END)  # Clear the contents of the entry widget
        self.e_passwd.insert(0, self.password)  # Insert the generated password


root = tk.Tk()
app = Login(root)
root.mainloop()
