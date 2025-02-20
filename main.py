from cryptography.fernet import Fernet, InvalidToken
import customtkinter
import tkinter as tk

#sets the appearace mode and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class PasswordManager(customtkinter.CTk):

    def __init__(self):

      #Initialisation Stuff
        super().__init__()
        self.key = None
        self.password_file = None
        self.password_dictionary = {}
        self.title("Password Manager Application")
        screen_width = self.winfo_screenwidth()
        self.geometry(f"1920x1080+{int((screen_width - 1920) / 2)}+0")


      #Buttons and messages
        self.welcomeMsg = customtkinter.CTkLabel(self, text="Welcome to my password manager application!",
                                                 font=("Century Gothic", int(screen_width / 80), "bold"))
        self.welcomeMsg.place(rely=0.025, relx=0.5, anchor="center")

        self.mainMsg = customtkinter.CTkLabel(self, text="Please choose the operation you wish to perform",
                                              font=("Century Gothic", int(screen_width / 80), ))
        self.mainMsg.place(rely=0.075, relx=0.5, anchor="center")

        self.createNewKeyBtn = customtkinter.CTkButton(self, height=300, width=300,
                                                       text="1. \n \n Create A New File Key",
                                                       command=self.create_a_key, corner_radius=50, fg_color="#C850C0",
                                                       font=("Century Gothic", int(screen_width / 70), "bold"))
        self.createNewKeyBtn.place(rely=0.15, relx=0.075)

        self.loadExistingKey = customtkinter.CTkButton(self, height=300, width=300, text="2. \n \n Load An Existing File Key",
                                                       command=self.load_key, corner_radius=50, fg_color="#70AD47",
                                                       font=("Century Gothic", int(screen_width / 70), "bold"))
        self.loadExistingKey.place(rely=0.15, relx=0.4)

        self.createNewPassFile = customtkinter.CTkButton(self, height=300, width=300, text="3. \n \n Create A New Password File",
                                                         command=self.create_pass_file, corner_radius=50, fg_color="#A7C7E7",
                                                         font=("Century Gothic", int(screen_width / 80), "bold"))
        self.createNewPassFile.place(rely=0.15, relx=0.725)

        self.loadExistingPassFile = customtkinter.CTkButton(self, height=300, width=300, text="4. \n \n Load Existing Password File",
                                                            command=self.load_password_file, corner_radius=50, fg_color="#D6A6D5",
                                                            font=("Century Gothic", int(screen_width / 80), "bold"))
        self.loadExistingPassFile.place(rely=0.55, relx=0.075)

        self.addPasstoFile = customtkinter.CTkButton(self, height=300, width=300, text="5. \n \n Add a New Password to File",
                                                     command=self.add_password, corner_radius=50, fg_color="#FFB3A7",
                                                     font=("Century Gothic", int(screen_width / 80), "bold"))
        self.addPasstoFile.place(rely=0.55, relx=0.4)

        self.getExistingPassword = customtkinter.CTkButton(self, height=300, width=300, text="6. \n \n Get an Existing Password",
                                                           command=self.get_password, corner_radius=50, fg_color="#E3A8C9",
                                                           font=("Century Gothic", int(screen_width / 70), "bold"))
        self.getExistingPassword.place(rely=0.55, relx=0.725)

        self.quitApplication = customtkinter.CTkButton(self, height=75, width=200, text="Exit Password Manager",
                                                       command=self.screen_kill, corner_radius=50,fg_color="#B24A4A", font=("Century Gothic", int(screen_width / 80), "bold"))
        self.quitApplication.place(rely=0.025, relx=0.75)

  #Function used to create a key that will be stored in a file
    def create_a_key(self):
        path = customtkinter.CTkInputDialog(text="What is the path you want for your key?").get_input()
        if path:
            self.key = Fernet.generate_key()
            with open(path, 'wb') as file:
                file.write(self.key)
                tk.messagebox.showinfo("System Message", f"Thanks!, Your key has been saved to {path}")
        else:
            print("No path entered. Key was not saved.")
#Function to load an already existing key so that it can be used to access password files later
    def load_key(self):
        path = customtkinter.CTkInputDialog(text="What is the path of your existing key").get_input()
        try:
            if path:
                with open(path, 'rb') as file:
                    self.key = file.read()
                    tk.messagebox.showinfo("System Message", f"Thanks!, The key in {path} has now been loaded!")
            if self.key is None:
                tk.messagebox.showerror("ERROR MESSAGE!", f"The Key didn't load correctly \n Please Try Again")
                return False
            return True
        except FileNotFoundError:
            tk.messagebox.showerror("ERROR MESSAGE!", f"There is no path called {path} \n Please try a different pathname")

  #Function to create a password file so that the user can store login information inside
    def create_pass_file(self):
        path = customtkinter.CTkInputDialog(text="What do you want your password file to be called?").get_input()
        if self.key is None:
            tk.messagebox.showerror("ERROR MESSAGE!", "No key has been loaded \n Please load a key first")
            return
        try:
            with open(path, 'w') as file:
                self.password_file = path
                tk.messagebox.showinfo("System Message", f"Thanks!, Your password file has been created :)")
        except Exception as e:
            tk.messagebox.showerror("ERROR MESSAGE!", "Error creating your password file, please try again")
          
#Function to access data inside an already existing password file 
    def load_password_file(self):
        path = customtkinter.CTkInputDialog(text="What is the password file that you wish to load?").get_input()
        if self.key is None:
            tk.messagebox.showerror("ERROR MESSAGE!", "No key has been loaded \n Please load a key first")
            return
        self.password_file = path
        try:
            with open(path, 'r') as file:
                for line in file:
                    site, encrypted = line.split(":")
                    try:
                        self.password_dictionary[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    except InvalidToken:
                        tk.messagebox.showerror(f"ERROR MESSAGE!", f"Invalid token for the following site {site}.com, password couldn't be decrypted")
            tk.messagebox.showinfo("System Message", f"Thanks!, Your password file has been loaded :)")
        except FileNotFoundError:
            tk.messagebox.showerror("ERROR MESSAGE!", "Password file not found. Please try again.")

  #Function to add passwords to a loaded password file
    def add_password(self):
        site = customtkinter.CTkInputDialog(text="What is the site name you want to store the password for?").get_input()
        password = customtkinter.CTkInputDialog(text="Enter the password please").get_input()
        if self.key is None:
            tk.messagebox.showerror(f"ERROR MESSAGE!", f"No key loaded. Please load a key first.")
            return
        self.password_dictionary[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as file:
                encrypted = Fernet(self.key).encrypt(password.encode())
                file.write(site + ":" + encrypted.decode() + "\n")
                tk.messagebox.showinfo("System Message", f"Password for {site} added successfully!")

  #function to request a specific password from a loaded personal password file
    def get_password(self):
        site = customtkinter.CTkInputDialog(text="Please enter the site name that you want the password for").get_input()
        if site:
            if site in self.password_dictionary:
                password = self.password_dictionary[site]
                tk.messagebox.showinfo("System Message",f"Password for {site}.com \n Your password is: {password}")
            else:
                tk.messagebox.showerror("ERROR MESSAGE!", f"No current password for this site. Please create one!")
        else:
            tk.messagebox.showwarning("Input Error", "You must enter a site name.")

#function to quit the application
    def screen_kill(self):
        tk.messagebox.showinfo("System Message", f"Thank You, See You Soon \n This program will now close :)")
        self.destroy()

if __name__ == "__main__":
    pm = PasswordManager()
    pm.mainloop()
