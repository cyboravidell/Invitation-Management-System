from tkinter import *
import sqlite3
from os import getcwd
from tkinter import messagebox

class Invitation:
    db_filename = 'user_data.db'
    def __init__(self,root) -> None:
        self.root = root
        table = "CREATE TABLE IF NOT EXISTS login_signup ( id INTEGER primary key,username TEXT,password TEXT,full_name TEXT,contact_number TEXT);"
        self.execute_db_query(table)
        print("table created")
        self.createlogin_signup()

    
    def createlogin_signup(self):

        # Sign-UP label
        labelFrame = LabelFrame(self.root, text="Create new User", bg="sky blue", font="helvetica 20 bold")
        labelFrame.grid(row=0,column=1, padx=8,pady=8, sticky=W)
        Label(labelFrame, text="Full Name: ", font="helvetica 15 bold", bg='green', fg="white").grid(row=1, column=1, sticky=W,padx=15,pady=2)
        self.nameField = Entry(labelFrame)
        self.nameField.grid(row=1,column=2,sticky=W,padx=5,pady=2)
        Label(labelFrame, text="User Name: ",font="helvetica 15 bold", bg="brown", fg="white").grid(row=2,column=1,sticky=W, padx=15, pady=2)
        self.userField = Entry(labelFrame)
        self.userField.grid(row=2,column=2, sticky=W, padx=5,pady=2)
        Label(labelFrame, text='Contact Number: ',font="helvetica 15 bold", bg="yellow",fg="white").grid(row=3, column=1, sticky=W, padx=15, pady=2)
        self.numField = Entry(labelFrame)
        self.numField.grid(row=3,column=2, sticky=W, padx=5,pady=2)
        Label(labelFrame, text='Password: ',font="helvetica 15 bold", bg="black",fg="white").grid(row=4, column=1, sticky=W, padx=15, pady=2)
        self.passField = Entry(labelFrame)
        self.passField.grid(row=4,column=2, sticky=W, padx=5,pady=2)
        Button(labelFrame, text='Create Account', command=self.on_create_account_button_clicked, bg="blue",fg="white").grid(row=5, column=2, sticky=E, padx=5,pady=5)

        # Sign-In Label

        labelFrame2 = LabelFrame(self.root, text="Sign - In", bg="sky blue", font="helvetica 20 bold")
        labelFrame2.grid(row=0,column=2, padx=8, sticky=E)
        Label(labelFrame2, text="Username: ", font="helvetica 15 bold", bg='green', fg="white").grid(row=1, column=1, sticky=W,padx=15,pady=2)
        self.userField2 = Entry(labelFrame2)
        self.userField2.grid(row=1,column=2,sticky=W,padx=5,pady=2)
        Label(labelFrame2, text="Password: ",font="helvetica 15 bold", bg="brown", fg="white").grid(row=2,column=1,sticky=W, padx=15, pady=2)
        self.passField2 = Entry(labelFrame2)
        self.passField2.grid(row=2,column=2, sticky=E, padx=5,pady=2)
        Button(labelFrame2, text='Log In', command=self.on_logIn_button_clicked, bg="blue",fg="white").grid(row=5, column=2, sticky=E, padx=5,pady=5)

    def on_create_account_button_clicked(self):
        self.add_new_user()

        pass

    def add_new_user(self):
        if self.new_user_validated():
            
            parameters = (self.userField.get(), self.passField.get(),self.nameField.get(),self.numField.get())
            query = f'INSERT INTO login_signup (username,password,full_name,contact_number) VALUES{parameters}'
            print(query)
            print(self.userField.get(),self.passField.get(),self.nameField.get(),self.numField.get(), sep=" ")
            self.execute_db_query(query)
            messagebox.showinfo("Complete", "New user added to database Successfully")
            self.nameField.delete(0, END)
            self.userField.delete(0, END)
            self.passField.delete(0, END)
            self.numField.delete(0, END)
            

        else:
            messagebox.showinfo("Error", "Name, number, user and password field can't blank")
        

    def new_user_validated(self):
        return len(self.nameField.get()) != 0 and len(self.userField.get()) != 0 and len(self.passField.get()) != 0

    def on_logIn_button_clicked(self):
        if self.existing_user_validated():
            try:
                query = f"select password from login_signup where username = '{self.userField2.get()}';"
                a = list(self.execute_db_query(query))[0][0]
                if a == self.passField2.get():
                    messagebox.showinfo("Successful", "Authentication Validated Successfully")
                    self.userField2.delete(0, END)
                    self.passField2.delete(0, END)
            except:
                messagebox.showinfo("Error", f"username - {self.userField2.get()} doesn't exist")
        
        else:
            messagebox.showinfo("Error", "username or password field can't blank")

    def existing_user_validated(self):
        return  len(self.userField2.get()) != 0 and len(self.passField2.get()) != 0

    

    def execute_db_query(self,query):
        with sqlite3.connect(self.db_filename)as conn:
            print(conn)
            print('You have successfuly connected to the Database')
            cursor = conn.cursor()
            query_result = cursor.execute(query)
            conn.commit()
        return query_result





if __name__ == '__main__':
    
    root  = Tk()
    root.title('My Invitation List')
    root.geometry("650x220")
    root.resizable(width=False, height=False)
    application = Invitation(root)
    root.mainloop()