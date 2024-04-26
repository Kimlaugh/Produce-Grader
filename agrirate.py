import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


root = None
signUp = None
home = None
grader1 = None
grader2 = None
tomatoLabel = None


def openRootWindow():      #Login Window
    global root, tomatoLabel
    if root:
        root.deiconify()
    else:
        root = tk.Tk()
        root.geometry("700x500")
        root.title("Login")

        def verifyLogin():
            email = emailInput.get() #get email address from input field
            password = pwInput.get() #get password from input field
            # if  password and email correct then:
            openHomeWindow()
            #else
            messagebox.showerror(message = "Incorrect email and/or password")
            # messageLabel = tk.Label(root, text="Incorrect email and/or password, Try Again") 
            # messageLabel.grid(row=5, column=0)


        # ------------------------------------------ ROOT DESIGN-----------------------------------------
        #LABELS
        agrirateLabel = tk.Label (root, text = "AgriRate")
        agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
        welcomeLabel = tk.Label (root, text = "Welcome to AgriRate")
        welcomeLabel.config(font =("Arial", 14), fg="#264D10")

        #BUTTONS
        signUpButton = tk.Button(root, text="Create an account here", fg="white", bg="#BF3100", command=openSignUpWindow)
        loginButton = tk.Button(root, text="Login", padx=50, pady=5, fg="#264D10", bg="#FFB316", command=verifyLogin)

        #ENTRY
        emailInput = tk.Entry(root, width=40)
        emailInput.configure(borderwidth=5)
        emailInput.insert(0, "Email")
    


        pwInput = tk.Entry(root, width=40)
        pwInput.configure(borderwidth=5)
        pwInput.insert(0, "Password")
    

        #CANVAS
        canvas=tk.Canvas(root, width=700, height=50, bg="#264D10")
        canvas.place(relx=0, rely=0)
        agrirateLabel.lift()
        signUpButton.lift()
        agrirateLabel.configure(bg=canvas['bg'])

        #PLACE
        agrirateLabel.place(relx=0.42, rely=0.01)
        signUpButton.place(relx=0.8, rely=0.03)
        welcomeLabel.place(relx=0.38, rely=0.2)
        loginButton.place(relx =0.42, rely=0.5)
        emailInput.place(relx=0.34, rely=0.3)
        pwInput.place(relx=0.34, rely= 0.4)

        #IMAGE
        if tomatoLabel is None:
            tomatoLogin = tk.PhotoImage(file="tomato.png")
            tomatoLabel = tk.Label(root, image=tomatoLogin)
            tomatoLabel.image = tomatoLogin
            tomatoLabel.place(relx =0, rely=0.6)
    

        def on_email_entry_click(event):
            if emailInput.get() == 'Email':
                emailInput.delete(0, "end") # delete all the text in the entry
                emailInput.insert(0, '') #Insert blank for user input
                emailInput.config(fg = 'black')
            
        def on_email_focusout(event):
            if emailInput.get() == '':
                emailInput.insert(0, 'Email')
                emailInput.config(fg = 'grey')

        def on_pw_entry_click(event):
            if pwInput.get() == 'Password':
                pwInput.delete(0, "end")
                pwInput.insert(0, '')
                pwInput.config(fg='black')

        def on_pw_focusout(event):
            if pwInput.get() == '':
                pwInput.insert(0, 'Password')
                pwInput.config(fg='grey')

                


        emailInput.bind('<FocusIn>', on_email_entry_click)
        emailInput.bind('<FocusOut>', on_email_focusout)
        pwInput.bind('<FocusIn>', on_pw_entry_click)
        pwInput.bind('<FocusOut>', on_pw_focusout)
        # ------------------------------------------------------------------------------------------------------------------------


def openSignUpWindow(): #Sign Up Window
    global signUp, tomatoLabel
    if signUp:
        signUp.deiconify()
    else:
        root.withdraw()
        signUp = tk.Toplevel(root)
        signUp.geometry("700x500")
        signUp.title("Sign Up")

        def backToRoot():
            signUp.withdraw()
            openRootWindow()

        # ---------------------------------------SIGN UP DESIGN-----------------------------------------------------------

        #LABELS
        agrirateLabel = tk.Label (signUp, text = "AgriRate")
        agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")

        #BUTTON
        signUpButton = tk.Button(signUp, text="Sign Up", padx=50, pady=5, fg="#264D10", bg="#FFB316", command=createAccount)
        back = tk.Button(signUp, text="Back", fg="white", bg="#BF3100", command=backToRoot)
        

        #ENTRY
        fNameInput = tk.Entry(signUp, width=40)
        fNameInput.insert(0, 'First Name')
        
        lNameInput = tk.Entry(signUp, width=40)
        lNameInput.insert(0, 'Last Name')
        
        emailInput = tk.Entry(signUp, width=40)
        emailInput.insert(0, 'Email')

        pwInput = tk.Entry(signUp, width=40)
        pwInput.insert(0, "Password")
        

        emailInput.configure(borderwidth=5)
        fNameInput.configure(borderwidth=5)
        lNameInput.configure(borderwidth=5)
        pwInput.configure(borderwidth=5)

        #CANVAS
        canvas=tk.Canvas(signUp, width=700, height=50, bg="#264D10")
        canvas.place(relx=0, rely=0)
        agrirateLabel.lift()
        back.lift()
        agrirateLabel.configure(bg=canvas['bg'])

        #PLACE
        agrirateLabel.place(relx=0.42, rely=0.01)
        fNameInput.place(relx=0.33, rely=0.15)
        lNameInput.place(relx=0.33, rely=0.25)
        emailInput.place(relx=0.33, rely=0.35)
        pwInput.place(relx=0.33, rely=0.45)
        signUpButton.place(relx=0.4, rely=0.52)
        back.place(relx=0.04, rely=0.03)

        #IMAGE
        tomatoLogin = tk.PhotoImage(file="tomato.png")
        tomatoLabel = tk.Label(signUp, image=tomatoLogin)
        tomatoLabel.image = tomatoLogin  # Retain reference to the image
        tomatoLabel.place(relx=0, rely=0.6)

        def on_email_entry_click(event):
            if emailInput.get() == 'Email':
                emailInput.delete(0, "end") # delete all the text in the entry
                emailInput.insert(0, '') #Insert blank for user input
                emailInput.config(fg = 'black')
            
        def on_email_focusout(event):
            if emailInput.get() == '':
                emailInput.insert(0, 'Email')
                emailInput.config(fg = 'grey')

        def on_pw_entry_click(event):
            if pwInput.get() == 'Password':
                pwInput.delete(0, "end")
                pwInput.insert(0, '')
                pwInput.config(fg='black')

        def on_pw_focusout(event):
            if pwInput.get() == '':
                pwInput.insert(0, 'Password')
                pwInput.config(fg='grey')

        def on_fName_entry_click(event):
            if fNameInput.get() == 'First Name':
                fNameInput.delete(0, "end")
                fNameInput.insert(0, '')
                fNameInput.config(fg='black')

        def on_fName_focusout(event):
            if fNameInput.get() == '':
                fNameInput.insert(0, 'First Name')
                fNameInput.config(fg='grey')

        
        def on_lName_entry_click(event):
            if lNameInput.get() == 'Last Name':
                lNameInput.delete(0, "end")
                lNameInput.insert(0, '')
                lNameInput.config(fg='black')

        def on_lName_focusout(event):
            if lNameInput.get() == '':
                lNameInput.insert(0, 'Last Name')
                lNameInput.config(fg='grey')

        fNameInput.bind('<FocusIn>', on_fName_entry_click)
        fNameInput.bind('<FocusOut>', on_fName_focusout)
        lNameInput.bind('<FocusIn>', on_lName_entry_click)
        lNameInput.bind('<FocusOut>', on_lName_focusout)
        emailInput.bind('<FocusIn>', on_email_entry_click)
        emailInput.bind('<FocusOut>', on_email_focusout)
        pwInput.bind('<FocusIn>', on_pw_entry_click)
        pwInput.bind('<FocusOut>', on_pw_focusout)


        # -----------------------------------------------------------------------------------------------------------------

def openHomeWindow():   #Home Window
    global home
    root.withdraw() 
    home = tk.Toplevel(root)
    home.geometry("700x500")
    home.title("Home")

    # ----------------------------------------------HOME DESIGN------------------------------------------------------------
    #LABELS
    homeLabel = tk.Label (home, text = "Welcome Back User!")
    homeLabel.config(font=("Arial", 14), fg="#BF3100")
    agrirateLabel = tk.Label (home, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")

    #BUTTON
    graderButton = tk.Button(home, text="Produce Grader", padx=290, pady=60, fg="#ffffff", bg="#FFB316", command=openProduceGrader1Window)
    logoutButton = tk.Button(home, text="Logout", fg="white", bg="#BF3100", command=logout)
    recordsButton = tk.Button(home, text="Produce Records", padx=287, pady=60, fg="#ffffff", bg="#FFB316")

    #CANVAS
    canvas=tk.Canvas(home, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    logoutButton.lift()
    agrirateLabel.configure(bg=canvas['bg'])

    #PLACE
    logoutButton.place(relx=0.9, rely=0.03)
    graderButton.place(relx=0.02, rely=0.25)
    recordsButton.place(relx=0.02, rely=0.6)
    homeLabel.place(relx=0.04, rely= 0.15)
    agrirateLabel.place(relx=0.42, rely=0.01)
    

def openProduceGrader1Window():
    global grader1, tomatoLabel
    if grader1:
        grader1.deiconify()
    else:
        home.withdraw()
        grader1 = tk.Toplevel(home)
        grader1.geometry("700x500")
        grader1.title("Produce Grader")

        def gradeMethod():
            selected_option = var.get()
            if selected_option == "Single":
                singleGrader()
                
            if selected_option == "Stock":
                stockGrader()


        def backToHome():
            grader1.withdraw()
            openHomeWindow()


        #-------------------------------DESIGN-----------------------------------------------------------
        #LABELS
        agrirateLabel = tk.Label (grader1, text = "AgriRate")
        agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
        graderLabel = tk.Label (grader1, text = "Produce Grader")
        graderLabel.config(font=("Arial", 14), fg="#BF3100")
        selectLabel= tk.Label(grader1, text = "Select a grading method")
        selectLabel.config(font=("Arial", 12))

        #BUTTONS
        homeButton = tk.Button(grader1, text="Home", fg="white", bg="#BF3100", command=backToHome)
        nextButton = tk.Button(grader1, text="Next", padx=50, pady=5, fg="#264D10", bg="#FFB316", command=gradeMethod)
        
        #CANVAS
        canvas=tk.Canvas(grader1, width=700, height=50, bg="#264D10")
        canvas.place(relx=0, rely=0)
        agrirateLabel.lift()
        homeButton.lift()
        agrirateLabel.configure(bg=canvas['bg'])

        #PLACE
        homeButton.place(relx=0.9, rely=0.03)
        graderLabel.place(relx=0.04, rely= 0.15)
        selectLabel.place(relx=0.38, rely=0.3)
        agrirateLabel.place(relx=0.42, rely=0.01)
        nextButton.place(relx=0.4, rely=0.48)

        #RADIO BUTTON
        var =tk.StringVar()
        var.set("Single")
        radio_button1 = tk.Radiobutton(grader1, text="Single", variable=var, value="Single")
        radio_button1.place(relx=0.37, rely=0.4)

        radio_button2 = tk.Radiobutton(grader1, text="Stock", variable=var, value="Stock")
        radio_button2.place(relx=0.55, rely=0.4)
        
        #IMAGE
        tomatoLogin = tk.PhotoImage(file="tomato.png")
        tomatoLabel = tk.Label(grader1, image=tomatoLogin)
        tomatoLabel.image = tomatoLogin  # Retain reference to the image
        tomatoLabel.place(relx=0, rely=0.6)



def singleGrader():
    global grader2, tomatoLabel
    selected_images = []

    def backToHome():
        grader2.withdraw()
        openHomeWindow()

    def backToGrader1():
        grader2.withdraw()
        openProduceGrader1Window()

    def uploadImage():
        if len(selected_images) == 3:
            messagebox.showinfo(message="Images successfully uploaded")
            #openSingleGrader2Window()
           
    
        # Ask user to select an image
        file_paths = filedialog.askopenfilenames(title="Choose an image of the produce")
    
        # If user cancels the selection
        if not file_paths: 
            messagebox.showerror(message="Please select an image.")
            return
    
        # If user selects more than 3 images
        if len(selected_images) + len(file_paths) > 3:
            messagebox.showerror(message = "You can only select three images.")
            return
    
        # Add selected images to the list
        selected_images.extend(file_paths)
    
        # Check if user has selected exactly 3 images
        if len(selected_images) == 3:
            messagebox.showinfo(message ="Images successfully uploaded.")
            #openSingleGrader2Window()
            
        

    if grader2:
        grader2.deiconify()
    else:
        grader1.withdraw()
        grader2 = tk.Toplevel(grader1)
        grader2.geometry("700x500")
        grader2.title("Produce Grader")


    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (grader2, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (grader2, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    promptLabel = tk.Label (grader2, text = "Upload 3 images of the produce in the order: side, other side, top view")
    promptLabel.config(font=("Arial", 12))

    #BUTTON
    homeButton = tk.Button(grader2, text="Home", fg="white", bg="#BF3100", command=backToHome)
    back = tk.Button(grader2, text="Back", fg="white", bg="#BF3100", command=backToGrader1)
    uploadButton= tk.Button(grader2, text="Upload Images",padx=50, pady=5, fg="#264D10", bg="#FFB316", command=uploadImage)

    #CANVAS
    canvas=tk.Canvas(grader2, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])
    homeButton.lift()
    back.lift()


    #PLACE
    agrirateLabel.place(relx=0.42, rely=0.01)
    homeButton.place(relx=0.9, rely=0.03)
    graderLabel.place(relx=0.04, rely= 0.15)
    promptLabel.place(relx=0.15, rely=0.36)
    back.place(relx=0.04, rely=0.03)
    uploadButton.place(relx=0.37, rely=0.45)

    #IMAGE
    # if tomatoLabel is None:
    tomatoLogin = tk.PhotoImage(file="tomato.png")
    tomatoLabel = tk.Label(grader2, image=tomatoLogin)
    tomatoLabel.image = tomatoLogin  # Retain reference to the image
    tomatoLabel.place(relx=0, rely=0.6)

















def createAccount():
    pass

def logout():
    home.withdraw()
    openRootWindow()



openRootWindow()

root.mainloop()