import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
import re
import os
import shutil
from . import classifcation_model
from . import Produce_Grading
import time


# key --


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
currentUser = dict()
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
    connection = mysql.connector.connect(
    host="localhost",
    user="capstone_user",
    password="12345678",
    database="capstone"
    )
    
    try:
        # update to connect database -- update_done
        if connection.is_connected():
            print("Connected to MySQL Server")
            return connection

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return False


def backToHome():
    global grader1, grader2, grader3, graderStock2, graderStock3, grader4, produceRecords
    if grader1:
        grader1.withdraw()
    if grader2:
        grader2.withdraw()
    if grader3:
        grader3.withdraw()
    if graderStock2:
        graderStock2.withdraw()
    if graderStock3:
        graderStock3.withdraw()
    if grader4:
        grader4.withdraw()
    if produceRecords:
        produceRecords.withdraw()
    
    # grader2.withdraw()
    openHomeWindow('Home') # -- update_done : added text inside function for all versions of it


def openRootWindow():      #Login Window
    global root, tomatoLabel
    if root:
        root.deiconify()
    else:
        root = tk.Tk()
        root.geometry("700x500")
        root.title("Login")

        # update to test the login function using real connection to database -- update_done 
        def verifyLogin():
            openHomeWindow("user: remove both lines")
            currentUser['user_id'] = 1
            return True
            email = emailInput.get() #get email address from input field
            password = pwInput.get() #get password from input field
            conn = connectToDB()
            if (conn):
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM user WHERE Email = %s AND Password = %s"
                cursor.execute(query, (email, password))
                row = cursor.fetchone()
                if row:
                    fname = row["FName"]
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

        # update database and check code below --
        def createAccount(fName, lName, email, pw):
            conn = connectToDB()
            if conn:
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
    # update: check if this code works --
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
    global tomatoLabel, grader1
    if home: # -- update: need to close home when other window is open
        home.withdraw() 
    
    if grader1:
        grader1.deiconify()
        pass
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


        # def backToHome():
        #     grader1.withdraw()
        #     openHomeWindow('Home')


        #-------------------------------DESIGN-----------------------------------------------------------
        #LABELS
        agrirateLabel = tk.Label (grader1, text = "AgriRate")
        agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
        graderLabel = tk.Label (grader1, text = "Produce Grader 1")
        graderLabel.config(font=("Arial", 14), fg="#BF3100")
        selectLabel= tk.Label(grader1, text = "Select a grading method")
        selectLabel.config(font=("Arial", 12))

        #BUTTONS
        homeButton = tk.Button(grader1, text="Home", fg="white", bg="#BF3100", command=backToHome)
        nextButton = tk.Button(grader1, text="Next 1", padx=50, pady=5, fg="#264D10", bg="#FFB316", command=gradeMethod)
        
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
    global grader2, tomatoLabel, grader1
    selected_images = []

    if grader1 and grader2:  # -- update_done : added if statement to remove the duplicate screen error
        grader1.withdraw()

    

    # def backToHome():
    #     grader2.withdraw()
    #     openHomeWindow('Home') # -- update_done : added text inside function for all versions of it

    def backToGrader1():
        grader2.withdraw()
        openProduceGrader1Window()

    def uploadImage(): #Save 1 image to database (the file name ending in side Example tomato_side)
        
        # if len(selected_images) == 3:
        #     messagebox.showinfo(message="Images successfully uploaded.")
        #     print (selected_images)
        #     # openProduceGrader3Window()
           
    
        # Ask user to select an image
        file_paths = filedialog.askopenfilenames(title="Choose an image of the produce")
    
        # If user cancels the selection
        if not file_paths: 
            messagebox.showerror(message="Please select an image.")
            return
    
        # If user selects more than 3 images
        if len(selected_images) + len(file_paths) > 3:  
        # if len(file_paths) != 3 :
            # clear the selected_images list
            selected_images.clear()   #-- update_done: 
            
            messagebox.showerror(message = "You can only select three images.")
            return
    
        # Add selected images to the list
        selected_images.extend(file_paths)
        uploadButton.config(text=f"Add {3 - len(selected_images) } More Images")
    
        # Check if user has selected exactly 3 images
        if len(selected_images) == 3:
            folder = "input_folder"
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                # Clear the contents of the folder
                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
            x = 0
            for s in selected_images:
               
                if os.path.exists(s):
                    image_filename = os.path.basename(s)
                    # You can modify the renaming logic here
                    if x == 0:
                        new_image_name = "produce_top.jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    else:
                        new_image_name = "produce_side" + str(x) + ".jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        img_for_classification = new_image_path
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    x += 1

            class_result = classifcation_model.predictor(img_for_classification,3,700)
            if (class_result['status']=="success"):
                produce_type = class_result['content']
                messagebox.showinfo(message = "Produce is: " + produce_type)
                # openProduceGrader3Window(produce_type, folder)
                grade_result = Produce_Grading.GetGrades(produce_type, folder)
                # time.sleep(2)
                if grade_result:
                    openProduceGrader4Window(grade_result, produce_type)
                #"Images successfully uploaded.") #-- update_done: so that code automatically goes to next window when 3 images are selected
            else:
                messagebox.showinfo(message = "There was an error: "+ {class_result['content']})#"Images successfully uploaded.") #-- update_done: so that code automatically goes to next window when 3 images are selected

            # openSingleGrader2Window()
            # openProduceGrader3Window() # -- update_done : so that conde automatically goes to next window when 3 images are selected
            

        

    if grader2:
        grader2.deiconify()
    else:
        grader1.withdraw()
        grader2 = tk.Toplevel(grader1)
        grader2.geometry("700x500")
        grader2.title("Produce Grader")


    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (grader2, text = "AgriRate v2")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (grader2, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    promptLabel = tk.Label (grader2, text = "Upload 3 images of the produce in the order: side, other side, top view")
    promptLabel.config(font=("Arial", 12))

    #BUTTON
    homeButton = tk.Button(grader2, text="Home", fg="white", bg="#BF3100", command=backToHome)
    back = tk.Button(grader2, text="Back 1", fg="white", bg="#BF3100", command=backToGrader1)
    uploadButton = tk.Button(grader2, text="Upload Images",padx=50, pady=5, fg="#264D10", bg="#FFB316", command=uploadImage)

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

# update check the loading screen --
def openProduceGrader3Window(produce_type, folder):    #Loading Screen- should be visible until grade is ready
    global grader3, grader2, graderStock2
    if grader3:
        grader3.deiconify()
    else:
        if grader2:
            grader2.withdraw()
        if graderStock2:
            graderStock2.withdraw()
        grader3 = tk.Toplevel(grader1)  
        grader3.geometry("700x500")
        grader3.title("Produce Grader")


    """ -- update_done: this was the original code: removed because it was causing errors --
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
    """
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
        image_path = f"loading/s{i}.png"
        frame = tk.PhotoImage(file=image_path)
        animation_frames.append(frame)

    # Start animation
    animate_loading(0)

    grade_result = Produce_Grading.GetGrades(produce_type, folder)
    # time.sleep(2)
    if grade_result:
        openProduceGrader4Window(grade_result, produce_type)

def openProduceGrader4Window(result, pType):   #Grade summary screen for single grader, displays after loading screen when grade is ready
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
    produceTypeLabel = tk.Label (grader4, text = "Crop: "+ pType)  #Replace with info from database
    produceTypeLabel.config(font=("Arial", 12))
    gradeLabel= tk.Label (grader4, text = "Grade: " + str(result))  #Replace with info from database
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
    segmentedImage = tk.PhotoImage(file="loading/s1.png")
    imageLabel = tk.Label(grader4, image=segmentedImage)
    imageLabel.image = segmentedImage
    imageLabel.place(relx =0.36, rely=0.15)


def stockGrader():  #if users select stock grading
    global graderStock2, tomatoLabel, grader1
    selected_images = []

    if grader1 and grader2:  # -- update_done : added if statement to remove the duplicate screen error
        grader1.withdraw()

    # def backToHome():
    #     graderStock2.withdraw()
    #     openHomeWindow('Home')

    

    def backToGrader1():
        
        graderStock2.withdraw()
        openProduceGrader1Window()

    def uploadImage():
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
            folder = "input_folder"
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                # Clear the contents of the folder
                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
            x = 0
            for s in selected_images:
                
                if os.path.exists(s):
                    image_filename = os.path.basename(s)
                    # You can modify the renaming logic here
                    if x == 0:
                        new_image_name = "produce_top.jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    else:
                        new_image_name = "produce_side" + str(x) + ".jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        img_for_classification = new_image_path
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    x += 1

            class_result = classifcation_model.predictor(img_for_classification,3,700)
            if (class_result['status']=="success"):
                produce_type = class_result['content']
                messagebox.showinfo(message = "Produce is: " + produce_type)
                # openProduceGrader3Window(produce_type, folder)
                grade_result = Produce_Grading.GetGrades(produce_type, folder)
                # time.sleep(2)
                if grade_result:
                    openStockGrader2Window(grade_result, produce_type)
                #"Images successfully uploaded.") #-- update_done: so that code automatically goes to next window when 3 images are selected
            else:
                messagebox.showinfo(message = "There was an error: "+ {class_result['content']})
            
        

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


def openStockGrader2Window(result, pType):  #summary screen for stock grader  (should loop until user selects done Loop: user goes back to grader3 then graderStock3 over and over)
    global graderStock3, tomatoLabel
    selected_images = []
    if graderStock3:
        graderStock3.deiconify()
    else:
        # grader3.withdraw()
        graderStock3 = tk.Toplevel(graderStock2) 
        graderStock3.geometry("700x500")
        graderStock3.title("Produce Grader")
    
    def uploadImage():
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
            folder = "input_folder"
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                # Clear the contents of the folder
                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
            x = 0
            for s in selected_images:
                
                if os.path.exists(s):
                    image_filename = os.path.basename(s)
                    # You can modify the renaming logic here
                    if x == 0:
                        new_image_name = "produce_top.jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    else:
                        new_image_name = "produce_side" + str(x) + ".jpg"  # Example: Adding 'new_' prefix
                        # Construct the new path within the new folder
                        new_image_path = os.path.join(folder, new_image_name)
                        img_for_classification = new_image_path
                        # Copy the image to the new folder with the new name
                        shutil.copy2(s,new_image_path)
                    x += 1

            class_result = classifcation_model.predictor(img_for_classification,3,700)
            if (class_result['status']=="success"):
                produce_type = class_result['content']
                messagebox.showinfo(message = "Produce is: " + produce_type)
                # openProduceGrader3Window(produce_type, folder)
                grade_result = Produce_Grading.GetGrades(produce_type, folder)
                # time.sleep(2)
                if grade_result:
                    openStockGrader2Window(grade_result, produce_type)
                #"Images successfully uploaded.") #-- update_done: so that code automatically goes to next window when 3 images are selected
            else:
                messagebox.showinfo(message = "There was an error: "+ {class_result['content']})
            

    #-------------------------------DESIGN-----------------------------------------------------------
    #LABELS
    agrirateLabel = tk.Label (graderStock3, text = "AgriRate")
    agrirateLabel.config(font=("Verdana", 20, "bold"), fg="white")
    graderLabel = tk.Label (graderStock3, text = "Produce Grader")
    graderLabel.config(font=("Arial", 14), fg="#BF3100")
    promptLabel = tk.Label (graderStock3, text = "Upload 3 images of the next produce in the order: side, other side, top view")
    produceTypeLabel = tk.Label (graderStock3, text = "Crop:" +pType) #Get from database
    produceGradeLabel = tk.Label (graderStock3, text = "Grade: "+ str(result)) #Get from database
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
    global produceRecords, home
    

    if produceRecords:
        produceRecords.deiconify()
    else:
        produceRecords = tk.Toplevel(home)  #change to home
        produceRecords.geometry("700x500")
        produceRecords.title("Produce Records")



    ############################ WORK IN PROGRESS ENDS ############################
    
    def deleteRecord(stock_id):
        # Function to handle delete action
        # Implement delete action here using idx to identify the item in the overview list
        # remove record from database
        conn = connectToDB()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = "DELETE FROM stock WHERE StockID = %s"
            cursor.execute(query, (idx,))
            conn.commit()
            cursor.close()
            conn.close()

        # Clear the canvas
        for widget in produceRecords.winfo_children():
            widget.destroy()

        

        openProduceRecordsWindow()


        print(f"Delete item at index {idx}")

    def editRecordWindow():
        popup = tk.Toplevel(produceRecords)
        popup.geometry("100x70")
        popup.title("Enter New Name of Stock")

        stockNameEntry = tk.Entry(popup, width=40)
        stockNameEntry.configure(borderwidth=5)
        stockNameEntry.place(relx = 0.2, rely=0.4)

        doneButton = tk.Button(popup, text="Update", fg="#264D10", bg="#FFB316", command = updateRecord)
        doneButton.place(relx= 0.5, rely=0.6)

        def updateRecord(old_name):
            # update implement code to update the stock name in the database -- update_done
            popup.withdraw()
            newName = stockNameEntry.get

            # added code below -- calvin 
            conn= connectToDB()
            if conn:
                cursor = conn.cursor(dictionary=True)
                query = "UPDATE stock SET Name = %s WHERE Name = %s"
                cursor.execute(query, (newName, old_name))
                conn.commit()
                cursor.close()
                


    # udpate implement code to update the stock name, date and time for grading that code is not correct below--

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
    reportButton = tk.Button(recordCanvas, text="Report", fg="#264D10", bg="#FFB316")#, command = openReportWindow)
    chartsButton = tk.Button(recordCanvas, text="Charts", fg="#264D10", bg="#FFB316")#, command = openChartsWindow)


    #################################################################### DISPLAY RECORDS ####################################################################
    # add a text field to enter stock name --update testing 
    # overview = [{"name": "Apple", "type": "Fruit"}, 
    #             {"name": "Carrot", "type": "Vegetable"}, 
    #             {"name": "Mango", "type": "Fruit"},
    #             {"name": "Red Onion", "type": "Vegetable"}]
    

    """ Stock table
    1	StockID	int(11)			No	None			    Change Change	    Drop Drop	
	2	Name	varchar(100)	utf8mb4_general_ci		No	None		    Change Change	Drop Drop	
	3	Count	int(11)			No	None			    Change Change	    Drop Drop	
	4	Date	datetime		No	None			    Change Change	    Drop Drop

    INSERT INTO `stock` (StockID,UserID,Name,Count,Date) VALUES 
    (1,1, 'Stock 1', 100, '2024-05-01 08:00:00'), 
    (2,1, 'Stock 2', 150, '2024-05-02 10:30:00'), 
    (3,1, 'Stock 3', 75, '2024-05-03 12:15:00'),
    (4,1, 'Stock 4', 200, '2024-05-04 14:45:00'),
    (5,1, 'Stock 5', 120, '2024-05-05 16:20:00');

    """

    # info needed:  Name, Date
    
    query = "SELECT StockID,name, date FROM stock WHERE UserID = %s"
    conn = connectToDB()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (currentUser['user_id'],))
        # cursor.execute(query)
        stocks = cursor.fetchall()
        cursor.close()
        conn.close()
    


    titleLabel = tk.Label(produceRecords, text="Produce Records Page")
    titleLabel.config(font=("Arial", 16), fg="black", bg="#ffffff")
    titleLabel.pack(pady=10)

    recordCanvas = tk.Canvas(produceRecords, width=670, height=1000, bg="#ffffff")
    recordCanvas.pack()

    
    # print(stocks)
    # def displayRecords(overview):
    for idx, item in enumerate(stocks):
        print(item)
        stock_id = int(item["StockID"])
        name = item["name"]
        date_ = item["date"]

        
        recordCanvas.create_text(30, 15 + idx * 70, anchor='nw', text=f"Name: {name}", font=("Arial", 14))
        recordCanvas.create_text(30, 35 + idx * 70, anchor='nw', text=f"Date: {date_}", font=("Arial", 10))

        edit_button = tk.Button(produceRecords, text="Edit", command=lambda idx=stock_id: edit_item(stock_id))
        edit_button.place(x=450, y=20 + idx * 70)

        delete_button = tk.Button(produceRecords, text="Delete", command=lambda idx=stock_id: deleteRecord(stock_id))
        delete_button.place(x=520, y=20 + idx * 70)

    # Function to handle edit action
    def edit_item(idx):
        # Implement edit action here using idx to identify the item in the overview list

        print(f"Edit item at index {idx}")

    

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
    records = []
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
