from tkinter import *
import sqlite3
from os import getcwd
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

class Invitation:
    db_filename = 'user_data.db'
    class InvitationData:
        db_filename = 'userInvitation_data.db'
        def __init__(self,root2, username) -> None:
            self.username = username
            table = f"CREATE TABLE IF NOT EXISTS {username} ( id INTEGER primary key,Name TEXT,City_or_Village TEXT, Number text,Relationship TEXT,Status TEXT);"
            self.execute_db_query(table)
            self.root2 = root2
            self.create_left_icon()
            self.add_new_person()
            self.create_message_area()
            self.create_tree_view()
            self.create_scrollbar()
            self.create_bottom_buttons()
            self.view_data()

        def create_left_icon(self):
            cwd = getcwd()
            print(cwd+'\Photos\ganesh.gif')
            photo = ImageTk.PhotoImage(Image.open("ganesh.jpg"))
            label = Label(self.root2,image=photo)
            label.grid(row=0,column=0)

        def add_new_person(self):

            # ADD new person label

            labelFrame = LabelFrame(self.root2, text="Add new Person", bg="sky blue", font="helvetica 10")
            labelFrame.grid(row=0,column=1, padx=8,pady=8, sticky="ew")
            Label(labelFrame, text="Full Name: ", bg='green', fg="white").grid(row=1, column=1, sticky=W,padx=15,pady=2)
            self.namefield = Entry(labelFrame)
            self.namefield.grid(row=1,column=2,sticky=W,padx=5,pady=2)
            Label(labelFrame, text="City/Village: ", bg="brown", fg="white").grid(row=2,column=1,sticky=W, padx=15, pady=2)
            self.addressfield = Entry(labelFrame)
            self.addressfield.grid(row=2,column=2, sticky=W, padx=5,pady=2)
            Label(labelFrame, text='Number: ', bg="black",fg="white").grid(row=3, column=1, sticky=W, padx=15, pady=2)
            self.numfield = Entry(labelFrame)
            self.numfield.grid(row=3,column=2, sticky=W, padx=5,pady=2)

            # Radio Button
            self.radio = StringVar()
            self.radio.set(None)
            self.radio2 = StringVar()
            self.radio2.set(None)
            Label(labelFrame, text='Relationship: ', bg="purple",fg="white").grid(row=4, column=1, sticky=W, padx=15, pady=2)
            self.r1 = Radiobutton(labelFrame, text = "SSP/Friend", variable = self.radio, value = "SSP/Friend", command=self.on_relationship_ssp_button_clicked).grid(row=4, column=2, sticky=W, padx=15, pady=2)
            self.r2 = Radiobutton(labelFrame, text = "Relative", variable = self.radio, value = "Relative", command=self.on_relationship_relative_button_clicked).grid(row=4, column=3, sticky=W, padx=15, pady=2)
            Label(labelFrame, text='Status: ', bg="brown",fg="white").grid(row=5, column=1, sticky=W, padx=15, pady=2)
            r3 = Radiobutton(labelFrame, text = "Invited", variable = self.radio2, value = "Invited", command=self.on_status_invited_button_clicked).grid(row=5, column=2, sticky=W, padx=15, pady=2)
            r4 = Radiobutton(labelFrame, text = "Uninvited", variable = self.radio2, value = "Uninvited", command=self.on_status_uninvited_button_clicked).grid(row=5, column=3, sticky=W, padx=15, pady=2)
            Button(labelFrame, text='Add Person', command=self.on_add_person_button_clicked, bg="blue",fg="white").grid(row=6, column=3, sticky=E, padx=5,pady=5)

        # Function of related Field

        def on_relationship_ssp_button_clicked(self):
            self.relatioField = self.radio.get()
            
        def on_relationship_relative_button_clicked(self):
            self.relatioField = self.radio.get()
           
        def on_status_invited_button_clicked(self):
            self.statusField = self.radio2.get()
          
        def on_status_uninvited_button_clicked(self):
            self.statusField = self.radio2.get()
            

        def on_add_person_button_clicked(self):
            
            if self.new_user_validated():

                parameters = (self.namefield.get(), self.addressfield.get(),self.numfield.get(),self.relatioField,self.statusField)
                query = f'INSERT INTO {self.username} (name,City_or_village,Number,Relationship,Status) VALUES{parameters};'
                self.execute_db_query(query)
                self.message['text'] = 'New Person {} added to the Database'.format(self.namefield.get())
                self.namefield.delete(0, END)
                self.addressfield.delete(0, END)
                self.numfield.delete(0, END)
                self.radio.set(None)
                self.radio2.set(None)

            else:
                self.message['text'] = 'Name, City/Village, Number etc. field cannot be blank'
            self.view_data()

        def new_user_validated(self):
            return len(self.namefield.get()) != 0 and len(self.numfield.get()) != 0 and len(self.statusField) != 0 and len(self.relatioField) != 0 and len(self.addressfield.get())

        def create_message_area(self):
            self.message = Label(self.root2,text='', fg="red")
            self.message.grid(row=3,column=1,sticky=W)

        def view_data(self):
            items = self.tree.get_children()
            for item in items:
                self.tree.delete(item)
            query = f'SELECT * FROM {self.username} order by name'
            contact_entries = self.execute_db_query(query)
            for row in contact_entries:
                self.tree.insert('',0, text=row[1], values=(row[2],row[3],row[4],row[5]))

        def create_tree_view(self):
            self.tree = ttk.Treeview(height=10, columns=("City/Village","Number","Relationship","Status"),style='Treeview')
            self.tree.grid(row=6,column=0,columnspan=5,padx=15)
            self.tree.heading("#0",text='Name',anchor=W)
            self.tree.heading("City/Village",text='City/Village',anchor=W)
            self.tree.heading("Number",text='Contact Number',anchor=W)
            self.tree.heading("Relationship",text='Relationship',anchor=W)
            self.tree.heading("Status",text='Status',anchor=W)
        
        def create_scrollbar(self):
            self.scrollbar = Scrollbar(orient='vertical',command=self.tree.yview)
            self.scrollbar.grid(row=6,column=6,rowspan=10,sticky='sn')
        
        def create_bottom_buttons(self):
            Button(text='Delete Selected', command=self.on_delete_selected_button_clicked,bg='red',fg="white").grid(row=8,column=0, sticky=W,padx=20,pady=10)
            Button(text="Modify Selected", command=self.on_modify_selected_button_clicked, bg="purple", fg="white").grid(row=8,column=1,sticky=W)

        def on_delete_selected_button_clicked(self):
            self.delete_contacts()
            
        def delete_contacts(self):
            self.message['text'] = ''
            name = self.tree.item(self.tree.selection())['text']
            query = f'DELETE FROM {self.username} where name = "{name}";'
            self.execute_db_query(query)
            self.message['text'] = f'Person  {name} deleted'
            self.view_data()

        def on_modify_selected_button_clicked(self):
            self.open_modify_window()

        def open_modify_window(self):
            name  = self.tree.item(self.tree.selection())['text']
            values = self.tree.item(self.tree.selection())['values']
            self.transient = Toplevel()
            self.transient.title('Update Person Details')
            
            labelFrame = LabelFrame(self.transient, text="Update Details", bg="sky blue", font="helvetica 10")
            labelFrame.grid(row=0,column=1, padx=8,pady=8, sticky="ew")
            Label(labelFrame, text="Full Name: ", bg='green', fg="white").grid(row=1, column=1, sticky=W,padx=15,pady=2)
            self.namefield = Entry(labelFrame,textvariable=StringVar(labelFrame, value=name))
            self.namefield.grid(row=1,column=2,sticky=W,padx=5,pady=2)
            Label(labelFrame, text="City/Village: ", bg="brown", fg="white").grid(row=2,column=1,sticky=W, padx=15, pady=2)
            self.addressfield = Entry(labelFrame,textvariable=StringVar(labelFrame, value=values[0]))
            self.addressfield.grid(row=2,column=2, sticky=W, padx=5,pady=2)
            Label(labelFrame, text='Number: ', bg="black",fg="white").grid(row=3, column=1, sticky=W, padx=15, pady=2)
            self.numfield = Entry(labelFrame,textvariable=StringVar(labelFrame, value=values[1]))
            self.numfield.grid(row=3,column=2, sticky=W, padx=5,pady=2)

            self.radio = StringVar()
            self.radio.set(None)
            self.radio2 = StringVar()
            self.radio2.set(None)
            Label(labelFrame, text='Relationship: ', bg="purple",fg="white").grid(row=4, column=1, sticky=W, padx=15, pady=2)
            self.r1 = Radiobutton(labelFrame, text = "SSP/Friend", variable = self.radio, value = "SSP/Friend", command=self.on_relationship_ssp_button_clicked).grid(row=4, column=2, sticky=W, padx=15, pady=2)
            self.r2 = Radiobutton(labelFrame, text = "Relative", variable = self.radio, value = "Relative", command=self.on_relationship_relative_button_clicked).grid(row=4, column=3, sticky=W, padx=15, pady=2)
            Label(labelFrame, text='Status: ', bg="brown",fg="white").grid(row=5, column=1, sticky=W, padx=15, pady=2)
            r3 = Radiobutton(labelFrame, text = "Invited", variable = self.radio2, value = "Invited", command=self.on_status_invited_button_clicked).grid(row=5, column=2, sticky=W, padx=15, pady=2)
            r4 = Radiobutton(labelFrame, text = "Uninvited", variable = self.radio2, value = "Uninvited", command=self.on_status_uninvited_button_clicked).grid(row=5, column=3, sticky=W, padx=15, pady=2)
            
            Button(labelFrame, text='Update Contact', command=lambda: self.update_contacts(name,values[0]), bg='black', fg='white').grid(row=6, column=3, sticky=E)
            self.transient.mainloop()
        
        def update_contacts(self,old_name,old_city_or_village):
            parameters = (self.namefield.get(), self.addressfield.get(),self.numfield.get(),self.relatioField,self.statusField)
            query = f'UPDATE {self.username} SET name="{parameters[0]}", City_or_Village = "{parameters[1]}",Number = "{parameters[2]}", Relationship = "{parameters[3]}", Status = "{parameters[4]}" where name = "{old_name}" and City_or_Village = "{old_city_or_village}";'
            self.execute_db_query(query)
            self.transient.destroy()
            self.message['text'] = f'Selected Person Details Modified'
            self.view_data()

        def execute_db_query(self,query):
            with sqlite3.connect(self.db_filename)as conn:
                print(conn)
                print('You have successfuly connected to the User Invitation Database')
                cursor = conn.cursor()
                query_result = cursor.execute(query)
                conn.commit()
            return query_result
    def __init__(self,root) -> None:
        self.root = root
        table = "CREATE TABLE IF NOT EXISTS login_signup ( id INTEGER primary key,username TEXT,password TEXT,full_name TEXT,contact_number TEXT);"
        self.execute_db_query(table)
        print(" Login table Loaded")
        self.createlogin_signup()
    
    def createApp2(self,userName):
        root2  = Tk()
        root2.title(f'{userName} Invitation List')
        root2.geometry("1050x500")
        # root2.resizable(width=False, height=False)
        application2 = self.InvitationData(root2,userName)
        root2.mainloop()

    
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

    def add_new_user(self):

        if self.new_user_validated():
            
            parameters = (self.userField.get(), self.passField.get(),self.nameField.get(),self.numField.get())
            query = f'INSERT INTO login_signup (username,password,full_name,contact_number) VALUES{parameters}'
    
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
                    username = self.userField2.get()
                    self.userField2.delete(0, END)
                    self.passField2.delete(0, END)

                    self.root.destroy()
                    self.createApp2(username)
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
    root.title('Log-In/ Sign-Up')
    root.geometry("650x220")
    # root.resizable(width=False, height=False)
    application = Invitation(root)
    root.mainloop()