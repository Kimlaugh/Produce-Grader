import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
import re

# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt

# # Create a tkinter window
# root = tk.Tk()
# root.geometry("600x400")

# # Create a matplotlib figure and subplot
# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# # Create a canvas
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas_widget = canvas.get_tk_widget()

# # Place the canvas in the window using relative positioning
# canvas_widget.place(relx=0, rely=0)

# # Run the tkinter event loop
# root.mainloop()



root = None
signUp = None
home = None
grader1 = None
grader2 = None
tomatoLabel = None
produceRecords = None
graderStock2 = None
graderStock3 = None
grader3 = None
grader4 = None


def connectToDB():
    try:
        connection = mysql.connector.connect(
            host='your_host',
            user='your_username',
            password='your_password',
            database='your_database_name'
        )
        if connection.is_connected():
            print("Connected to MySQL Server")
            return [True , connection]

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return [False, 0]


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
            connect_check = connectToDB
            if (connect_check[0]):
                conn = connect_check[1]
                cursor = conn.cursor()
                query = "SELECT * FROM user WHERE Email = %s AND Password = %s"
                cursor.execute(query, (email, password))
                row = cursor.fetchone()
                if row:
                    fname = row[1]
                    openHomeWindow(fname)
                else:
                    messagebox.showerror(message = "Incorrect email and/or password")
                
                cursor.close()
                conn.close()
            else:
                messagebox.showerror(message="Failed to connect to the database")
                

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

        def createAccount(fName, lName, email, pw):
            connect_check = connectToDB
            if (connect_check[0]):
                conn = connect_check[1]
                cursor = conn.cursor()
                query = "INSERT INTO user (FName, LName, Email, Password) VALUES (%s, %s, %s, %s)"
                data = (fName, lName, email, pw)
                cursor.execute(query, data)
                conn.commit()

                cursor.close()
                conn.close()
                messagebox.showinfo(message = "Account successfully created, login to continue")
                backToRoot()
            else:
                messagebox.showerror(message="Failed to create account")

        def ValidateInputs():
            #validation done here
            email = emailInput.get()
            pw = pwInput.get()
            fname = fNameInput.get()
            lname = lNameInput.get()
            email = emailInput.get()
    
            # Validate email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                # If email is invalid, show error message and return
                messagebox.showerror(message= "Invalid email address")
                return
            
            # Validate first name
            name_pattern = r'^[a-zA-Z]+$'
            if not re.match(name_pattern, fname):
                # If first name is invalid, show error message and return
                messagebox.showerror(message= "First name can only contain letters")
                return
            
            # Validate last name
            if not re.match(name_pattern, lname):
                # If last name is invalid, show error message and return
                messagebox.showerror(message= "Last name can only contain letters")
                return
            
            # If success, call createAccount with validated inputs
            
            createAccount(fname, lname, email, pw)

        # ---------------------------------------SIGN UP DESIGN-----------------------------------------------------------

        #LABELS
        agrirateLabel = tk.Label (signUp, text = "AgriRate")
        agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")

        #BUTTON
        signUpButton = tk.Button(signUp, text="Sign Up", padx=50, pady=5, fg="#264D10", bg="#FFB316", command=ValidateInputs)
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

def openHomeWindow(name):   #Home Window
    global home
    root.withdraw() 
    home = tk.Toplevel(root)
    home.geometry("700x500")
    home.title("Home")

    # ----------------------------------------------HOME DESIGN------------------------------------------------------------
    #LABELS
    homeLabel = tk.Label (home, text = "Welcome Back " + name)
    homeLabel.config(font=("Arial", 14), fg="#BF3100")
    agrirateLabel = tk.Label (home, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")

    #BUTTON
    graderButton = tk.Button(home, text="Produce Grader", padx=290, pady=60, fg="#ffffff", bg="#FFB316", command=openProduceGrader1Window)
    logoutButton = tk.Button(home, text="Logout", fg="white", bg="#BF3100", command=logout)
    recordsButton = tk.Button(home, text="Produce Records", padx=287, pady=60, fg="#ffffff", bg="#FFB316", command=openProduceRecordsWindow)

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
    

def openProduceGrader1Window():  #Users select grading method
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



def singleGrader():  #if users select single grading
    global grader2, tomatoLabel
    selected_images = []

    def backToHome():
        grader2.withdraw()
        openHomeWindow()

    def backToGrader1():
        grader2.withdraw()
        openProduceGrader1Window()

    def uploadImage(): #Save 1 image to database (the file name ending in side Example tomato_side)
        if len(selected_images) == 3:
            messagebox.showinfo(message="Images successfully uploaded")

            openProduceGrader3Window()
           
    
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


def openProduceGrader3Window():    #Loading Screen- should be visible until grade is ready
    global grader3
    if grader3:
        grader3.deiconify()
    else:
        grader2.withdraw() 
        graderStock2.withdraw()
        grader3 = tk.Toplevel(grader1)  
        grader3.geometry("700x500")
        grader3.title("Produce Grader")

    
    #--------------------------------------GRADER 3 DESIGN------------------------------------
    #LABELS
    agrirateLabel = tk.Label (grader3, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (grader3, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    progressLabel = tk.Label(grader3, text = "Grading in Progress")
    progressLabel.config(font=("Arial", 14))

    

    #CANVAS
    canvas=tk.Canvas(grader3, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])

    #PLACE
    graderLabel.place(relx=0.04, rely= 0.15)
    agrirateLabel.place(relx=0.42, rely=0.01)
    progressLabel.place(relx=0.38, rely=0.7)
    
    loading_canvas = tk.Canvas(grader3, width=100, height=100, bg="white")
    loading_canvas.place(relx=0.42, rely=0.4)



    def animate_loading(index):
        loading_canvas.delete("all")
        loading_canvas.create_image(50, 50, image=animation_frames[index], anchor="center")
        index = (index + 1) % len(animation_frames)
        grader3.after(100, animate_loading, index)

    # Load animation frames
    animation_frames = []
    for i in range(1, 9):
        image_path = f"s{i}.png"
        frame = tk.PhotoImage(file=image_path)
        animation_frames.append(frame)

    # Start animation
    animate_loading(0)

def openProduceGrader4Window():   #Grade summary screen for single grader, displays after loading screen when grade is ready
    global grader4
    if grader4:
        grader4.deiconify()
    else:
        #grader3.withdraw()
        grader4 = tk.Toplevel(grader2)  
        grader4.geometry("700x500")
        grader4.title("Produce Grader")

    

    #----------------------------------------GRADER 4 DESIGN----------------------------------
    #LABELS
    agrirateLabel = tk.Label (grader4, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (grader4, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    produceTypeLabel = tk.Label (grader4, text = "Crop: Carrot")  #Replace with info from database
    produceTypeLabel.config(font=("Arial", 12))
    gradeLabel= tk.Label (grader4, text = "Grade: 2")  #Replace with info from database
    gradeLabel.config(font=("Arial", 12))

    #BUTTON
    doneButton = tk.Button(grader4, text="Done", padx=50, pady=5, fg="#264D10", bg="#FFB316") #command = generateReport)
    
    #CANVAS
    canvas=tk.Canvas(grader4, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])


    #PLACE 
    agrirateLabel.place(relx=0.42, rely=0.01)
    graderLabel.place(relx=0.04, rely= 0.15)
    doneButton.place(relx=0.42, rely= 0.85)
    produceTypeLabel.place(relx=0.45, rely= 0.68)
    gradeLabel.place(relx=0.465, rely= 0.78)

    #IMAGE get segmented image from database
    segmentedImage = tk.PhotoImage(file="s1.png")
    imageLabel = tk.Label(grader4, image=segmentedImage)
    imageLabel.image = segmentedImage
    imageLabel.place(relx =0.36, rely=0.15)


def stockGrader():  #if users select stock grading
    global graderStock2, tomatoLabel
    selected_images = []

    def backToHome():
        graderStock2.withdraw()
        openHomeWindow()

    def backToGrader1():
        graderStock2.withdraw()
        openProduceGrader1Window()

    def uploadImage():
        if len(selected_images) == 3:
            messagebox.showinfo(message="Images successfully uploaded")
            openProduceGrader3Window()
            
    
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
            openProduceGrader3Window()
            
        

    if graderStock2:
        graderStock2.deiconify()
    else:
        grader1.withdraw()
        graderStock2 = tk.Toplevel(grader1)
        graderStock2.geometry("700x500")
        graderStock2.title("Produce Grader")


    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (graderStock2, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (graderStock2, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    promptLabel = tk.Label (graderStock2, text = "Upload 3 images of the first produce in the order: side, other side, top view")
    promptLabel.config(font=("Arial", 12))
    promptLabel2 = tk.Label (graderStock2, text = "Enter a name for the stock")
    promptLabel2.config(font=("Arial", 12))

    #ENTRY
    stockNameInput = tk.Entry(graderStock2, width=40)
    stockNameInput.configure(borderwidth=5)
    stockNameInput.insert(0, "Stock Name")

    #BUTTON
    homeButton = tk.Button(graderStock2, text="Home", fg="white", bg="#BF3100", command=backToHome)
    back = tk.Button(graderStock2, text="Back", fg="white", bg="#BF3100", command=backToGrader1)
    uploadButton= tk.Button(graderStock2, text="Upload Images",padx=50, pady=5, fg="#264D10", bg="#FFB316", command=uploadImage)

    #CANVAS
    canvas=tk.Canvas(graderStock2, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])
    homeButton.lift()
    back.lift()


    #PLACE
    agrirateLabel.place(relx=0.42, rely=0.01)
    homeButton.place(relx=0.9, rely=0.03)
    graderLabel.place(relx=0.04, rely= 0.15)
    promptLabel.place(relx=0.15, rely=0.45)
    promptLabel2.place(relx=0.38, rely=0.23)
    back.place(relx=0.04, rely=0.03)
    uploadButton.place(relx=0.37, rely=0.53)
    stockNameInput.place(relx=0.33, rely=0.33)

    #IMAGE
    # if tomatoLabel is None:
    tomatoLogin = tk.PhotoImage(file="tomato.png")
    tomatoLabel = tk.Label(graderStock2, image=tomatoLogin)
    tomatoLabel.image = tomatoLogin  # Retain reference to the image
    tomatoLabel.place(relx=0, rely=0.6)

    def on_stock_entry_click(event):
        if stockNameInput.get() == 'Stock Name':
            stockNameInput.delete(0, "end") # delete all the text in the entry
            stockNameInput.insert(0, '') #Insert blank for user input
            stockNameInput.config(fg = 'black')
            
    def on_stock_focusout(event):
        if stockNameInput.get() == '':
            stockNameInput.insert(0, 'Stock Name')
            stockNameInput.config(fg = 'grey')
    
    stockNameInput.bind('<FocusIn>', on_stock_entry_click)
    stockNameInput.bind('<FocusOut>', on_stock_focusout)


def openStockGrader2Window():  #summary screen for stock grader  (should loop until user selects done Loop: user goes back to grader3 then graderStock3 over and over)
    global graderStock3, tomatoLabel
    if graderStock3:
        graderStock3.deiconify()
    else:
        grader3.withdraw()
        graderStock3 = tk.Toplevel(graderStock2) 
        graderStock3.geometry("700x500")
        graderStock3.title("Produce Grader")
    
    def uploadImage():
        pass

    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (graderStock3, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (graderStock3, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    promptLabel = tk.Label (graderStock3, text = "Upload 3 images of the next produce in the order: side, other side, top view")
    produceTypeLabel = tk.Label (graderStock3, text = "Crop: Carrot") #Get from database
    produceGradeLabel = tk.Label (graderStock3, text = "Grade: 2") #Get from database
    produceGradeLabel.config(font=("Arial", 12))
    produceTypeLabel.config(font=("Arial", 12))
    promptLabel.config(font=("Arial", 12))

    #BUTTON
    doneButton = tk.Button(graderStock3, text="Done", fg="white", bg="#BF3100") #command=generateReport)
    gradeButton= tk.Button(graderStock3, text="Grade",padx=50, pady=5, fg="#264D10", bg="#FFB316", command=openProduceGrader3Window)
    uploadButton= tk.Button(graderStock3, text="Upload Images",padx=50, pady=5, fg="#264D10", bg="#FFB316", command=uploadImage)
    
    #CANVAS
    canvas=tk.Canvas(graderStock3, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])


    #TOMATO IMAGE
    tomatoLogin = tk.PhotoImage(file="tomato.png")
    tomatoLabel = tk.Label(graderStock3, image=tomatoLogin)
    tomatoLabel.image = tomatoLogin  # Retain reference to the image
    tomatoLabel.place(relx=0, rely=0.6)

    # #SEGMENTED IMAGE
    # segmentedImage = tk.PhotoImage(file="s1.png")
    # imageLabel = tk.Label(graderStock3, image=segmentedImage)
    # imageLabel.image = segmentedImage
    # imageLabel.place(relx =0.1, rely=0.1)

    #PLACE
    agrirateLabel.place(relx=0.42, rely=0.01)
    produceTypeLabel.place(relx=0.35, rely=0.25)
    produceGradeLabel.place(relx=0.35, rely=0.3)
    graderLabel.place(relx=0.04, rely= 0.15)
    promptLabel.place(relx=0.15, rely=0.47)
    uploadButton.place(relx=0.37, rely=0.53)
    doneButton.place(relx=0.9, rely=0.28)


def openProduceRecordsWindow():   #Window that displays produce records
    global produceRecords
    if produceRecords:
        produceRecords.deiconify()
    else:
        produceRecords = tk.Toplevel(root)  #change to home
        produceRecords.geometry("700x500")
        produceRecords.title("Produce Records")
    
    def backToHome():
        produceRecords.withdraw()
        openHomeWindow()
    
    def deleteRecord():
        pass

    def editRecordWindow():
        popup = tk.Toplevel(produceRecords)
        popup.geometry("100x70")
        popup.title("Enter New Name of Stock")

        stockNameEntry = tk.Entry(popup, width=40)
        stockNameEntry.configure(borderwidth=5)
        stockNameEntry.place(relx = 0.2, rely=0.4)

        doneButton = tk.Button(popup, text="Update", fg="#264D10", bg="#FFB316", command = updateRecord)
        doneButton.place(relx= 0.5, rely=0.6)

        def updateRecord():
            popup.withdraw()
            newName = stockNameEntry.get

        
    # def getUserRecords():
    #     connect_check = connectToDB
    #     if (connect_check[0]):
    #         conn = connect_check[1]
    #         cursor = conn.cursor()
    #         query = "SELECT * FROM user WHERE Email = %s
    #         cursor.execute(query, (email))
    #         records = cursor.fetchall()
                
    #         cursor.close()
    #         conn.close()


    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (produceRecords, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    titleLabel = tk.Label (produceRecords, text = "My Produce Records")
    titleLabel.config(font=("Arial", 14), fg="#BF3100")

    #BUTTON
    homeButton = tk.Button(produceRecords, text="Home", fg="white", bg="#BF3100", command=backToHome)
    recordCanvas = tk.Canvas(produceRecords, width=670, height=70, bg="#264D10")
    editButton = tk.Button(recordCanvas, text="Edit", fg="#264D10", bg="#FFB316", command = editRecordWindow)
    deleteButton = tk.Button(recordCanvas, text="Delete", fg="white", bg="#BF3100", command = deleteRecord)
    reportButton = tk.Button(recordCanvas, text="Report", fg="#264D10", bg="#FFB316", command = openReportWindow)
    chartsButton = tk.Button(recordCanvas, text="Charts", fg="#264D10", bg="#FFB316", command = openChartsWindow)

    #CANVAS
    canvas=tk.Canvas(produceRecords, width=700, height=50, bg="#264D10")
    canvas.place(relx=0, rely=0)
    agrirateLabel.lift()
    agrirateLabel.configure(bg=canvas['bg'])
    homeButton.lift()

    #PLACE
    agrirateLabel.place(relx=0.42, rely=0.01)
    homeButton.place(relx=0.9, rely=0.03)
    titleLabel.place(relx=0.04, rely= 0.15)

    # Display records
    #if records exist for user:
    for record in records:
        recordCanvas = tk.Canvas(produceRecords, width=670, height=70, bg="#264D10")
       
        recordCanvas.create_text(30, 15, anchor='nw', text=f"Name: {record[0]}",font=("Arial", 14))  #Stock name or name of produce 
        recordCanvas.create_text(30, 35, anchor='nw', text=f"Date: {record[1]}", font=("Arial", 10))
        recordCanvas.create_text(30, 50, anchor='nw', text=f"Time: {record[2]}", font=("Arial", 10))
        recordCanvas.create_window(560, 40, window=reportButton)
        recordCanvas.create_window(505, 40, window=chartsButton)
        recordCanvas.create_window(615, 40, window=deleteButton)
        
        # if record is a stock then:
        recordCanvas.create_window(450, 40, window=editButton)
    
        recordCanvas.pack(padx=10, pady=10)
    #else
        # messagebox.showinfo(message ="You have no produce records")



def logout():
    home.withdraw()
    openRootWindow()



openRootWindow()

root.mainloop()