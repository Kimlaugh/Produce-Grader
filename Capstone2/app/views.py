import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm, UploadForm, RegisterForm
from flask import send_from_directory
from flask_login import logout_user
from datetime import datetime
import secrets
import mysql.connector
import os
import shutil
import base64
import re
from email import message_from_string
from flask import Flask, request, jsonify
# from . import agrirate 
from . import classifcation_model
from . import Produce_Grading
import datetime



# You will need to import the appropriate function to do so.
from werkzeug.security import check_password_hash

###
# Routing for your application.
###

# @app.route('/')
# def home():
#     """Render website's home page."""

#     return render_template('home.html')


@app.route('/')
def home():
    """Render website's home page."""

    return render_template('capstoneHome.html')
    # return render_template('home.html', name="Test")

@app.route('/home')
def mainPage():
    global user_stock
    global stock_id
    conn = connectToDB()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM produce WHERE StockID = %s "
        cursor.execute(query, (stock_id,))
        rows = cursor.fetchall()
        count = len(rows)
        print(count)
        insert_query = "UPDATE stock SET Count = %s WHERE StockID = %s"
        cursor.execute(insert_query, (count, stock_id))
        conn.commit()

        cursor.close()
        conn.close()
    user_stock = []
    stock_id = None
    """Render website's home page."""

    # Directory path
    images_directory = "app/static/images"

    # Get list of all files in the directory
    files = os.listdir(images_directory)

    # Iterate through each file
    for file in files:
        # Check if file is an image and contains the word "side" in its filename
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and 'side' in file.lower():
            # Construct full path to the file
            file_path = os.path.join(images_directory, file)
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

    # return render_template('capstoneHome.html')
    return render_template('home.html', name="Test")

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/register/', methods=['POST', 'GET'])
def register():    
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            
            return render_template('register.html', form=form)
        else:
            conn = connectToDB()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user (FName, LName, Email, Password) VALUES (%s, %s, %s, %s)", (form.firstname.data, form.lastname.data, form.email.data, form.password.data))
                conn.commit()
                cursor.close()
                conn.close()
            flash('Record was successfully added')
           
            return render_template('home.html', name = form.firstname.data)
    return render_template('register.html', form=form)
@app.route('/stockName', methods=['POST', 'GET'])
def getStockName():
    return render_template('StockName.html', grad_type = "single")

@app.route('/upload', methods=['POST', 'GET'])
# @login_required
def upload():
    return render_template('upload.html', grad_type = "single")

stock_name = ""
stock_id = 0

@app.route('/upload/stock', methods=['POST', 'GET'])
# @login_required
def uploadStock():
    global stock_name
    global user_id
    stock_name = request.form['stock_name']

    current_date = datetime.datetime.now().date()

    conn = connectToDB()
    if (conn):
        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO stock (UserID, Name, Count, Date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, stock_name, 0, current_date))
        conn.commit()

        # Get the last inserted ID
        cursor.execute("SELECT LAST_INSERT_ID()")
        global stock_id
        stock_id = cursor.fetchone()
        stock_id = stock_id['LAST_INSERT_ID()']
        cursor.close()
        conn.close()
    else:
        flash('Eerror connecting to database', 'error')

    
    print(stock_name)
    return render_template('upload.html', grad_type = "stock")

@app.route('/upload/stockAgain')
def uploadStockAgain():
    return render_template('upload.html', grad_type = "stock")


@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        # Get the image paths from the request
        data = request.get_json()
        image_data_uris = data.get('imagePaths', [])
        
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
                    print(f"Failed to delete {file_path}. Reason: {e}")

        for i, image_data_uri in enumerate(image_data_uris):
            # Decode Base64 image data
            header, image_data = image_data_uri.split(',', 1)

            # Parse header to extract filename
            # Extract filename from URI
            filename_match = re.search(r'filename=([^;]+)', image_data_uri)
            filename = filename_match.group(1) if filename_match else None
            print(filename)

            image_binary = base64.b64decode(image_data)

            # Determine the file name based on the image index
            if i == 0:
                new_image_name = "produce_top.jpg"
                # keywords = ["tomato", "carrot", "pepper"]
                # matched_keyword = next((keyword for keyword in keywords if keyword in filename), None)
                # if matched_keyword:
                #     new_image_name = matched_keyword + "_top.jpg"
            else:
                new_image_name = f"produce_side{i}.jpg"
                # keywords = ["tomato", "carrot", "pepper"]
                # matched_keyword = next((keyword for keyword in keywords if keyword in filename), None)
                # if matched_keyword:
                #     new_image_name = matched_keyword + f"_side{i}.jpg"
                # new_image_path = os.path.join(folder, new_image_name)
                # img_for_classification = new_image_path

            # Save the image to the folder
            new_image_path = os.path.join(folder, new_image_name)
            with open(new_image_path, 'wb') as f:
                f.write(image_binary)

        return jsonify({'message': 'Images received and saved successfully'}), 200

    # return render_template('home.html')


@app.route('/grade')
def grade():
    # List all files in the input folder
    folder_path = 'input_folder'
    img_for_classification = ''

    files = os.listdir(folder_path)
    # Look for a JPG file containing the word "side" in its name
    side_image = None
    for file in files:
        if file.lower().endswith('.jpg') and 'side' in file.lower():
            side_image = os.path.join(folder_path, file)
            file_name = file
            break
    
    if side_image is None:
        print("No JPG file with 'side' in its name found.")
    else:
        # print("Found side image:", side_image)
        img_for_classification = side_image
        absolute_path = os.path.abspath(side_image)


    class_result = classifcation_model.predictor(img_for_classification,3,700)
    grade_result = img_for_classification
    keywords = ["tomato", "carrot", "pepper"]
    matched_keyword = next((keyword for keyword in keywords if keyword in file_name), None)
    print(matched_keyword)
    if class_result['status'] == "success" or class_result['content'] == "Confidence":
        if (class_result['content'] == "Confidence"):
            produce_type = "pepper"
        else:
            produce_type = class_result['content']
        print (produce_type)
        grade_result = Produce_Grading.GetGrades(produce_type, folder_path)
        # time.sleep(2)
        # Define paths
        input_folder = "input_folder"  # Change this to the actual name of your input folder
        output_folder = "app/static/images"  # The destination folder inside the static folder
        image_filename = file_name  # The name of the image file you want to copy

        # Ensure output folder exists, if not create it
        os.makedirs(output_folder, exist_ok=True)

        # Construct full paths
        source_path = os.path.join(input_folder, image_filename)
        destination_path = os.path.join(output_folder, image_filename)

        # Copy the image file
        shutil.copyfile(source_path, destination_path)

        grade_result['type'] = produce_type.upper()
        grade_result['img'] = file_name

        return render_template("singleSummary.html", grade=grade_result)
    else:
        flash("This is not a recognised Produce")
        print (class_result['content'])
        return render_template('upload.html', grad_type = "single")
    
user_stock = []

@app.route('/grade/stock')
def gradeStock():
    global user_stock
    # List all files in the input folder
    folder_path = 'input_folder'
    img_for_classification = ''

    files = os.listdir(folder_path)
    # Look for a JPG file containing the word "side" in its name
    side_image = None
    for file in files:
        if file.lower().endswith('.jpg') and 'side' in file.lower():
            side_image = os.path.join(folder_path, file)
            file_name = file
            break
    
    if side_image is None:
        print("No JPG file with 'side' in its name found.")
    else:
        # print("Found side image:", side_image)
        img_for_classification = side_image
        absolute_path = os.path.abspath(side_image)


    class_result = classifcation_model.predictor(img_for_classification,3,700)
    grade_result = img_for_classification
    keywords = ["tomato", "carrot", "pepper"]
    matched_keyword = next((keyword for keyword in keywords if keyword in file_name), None)
    if class_result['status'] == "success" or class_result['content'] == "Confidence":
        if (class_result['content'] == "Confidence"):
            # print (matched_keyword)
            produce_type = "pepper"
        else:
            produce_type = class_result['content']
        print (produce_type)
        # return render_template("StockSummary.html", grade=user_stock)
        grade_result = Produce_Grading.GetGrades(produce_type, folder_path)
        # time.sleep(2)
        # Define paths
        input_folder = "input_folder"  # Change this to the actual name of your input folder
        output_folder = "app/static/images"  # The destination folder inside the static folder
        image_filename = file_name  # The name of the image file you want to copy

        # Ensure output folder exists, if not create it
        os.makedirs(output_folder, exist_ok=True)

        # Split the file name into base name and extension
        base_name, extension = file_name.rsplit('.', 1)

        new_file_name = base_name+"_"+str(len(user_stock))+"."+extension

        # Construct full paths
        source_path = os.path.join(input_folder, image_filename)
        destination_path = os.path.join(output_folder, new_file_name)

        # Copy the image file
        shutil.copyfile(source_path, destination_path)

        

        # Insert the number before the extension
        
        grade_result['type'] = produce_type.upper()
        grade_result['img'] = new_file_name
        user_stock.append(grade_result)

        conn = connectToDB()
        global stock_id
        if (conn):
            cursor = conn.cursor(dictionary=True)
            query = "INSERT INTO produce (StockID, Type, Grade) VALUES (%s, %s, %s)"
            cursor.execute(query, (stock_id, produce_type, grade_result['final']))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            flash('Eerror connecting to database', 'error')

        return render_template("StockSummary.html", grade=user_stock[-1])
    else:
        flash("This is not a recognised Produce")
        print (class_result['content'])
        return render_template('upload.html', grad_type = "stock")
            
        

    
    

user_id = 10
@app.route('/login', methods=['POST', 'GET'])
def login():
    
    email = request.form['email']
    password = request.form['password']

    print ("Login info", email, password)
    conn = connectToDB()

    if (conn):
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM user WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        row = cursor.fetchone()
        if row:
            fname = row["FName"]
            global user_id
            user_id = row["UserID"]
            cursor.close()
            conn.close()
            return render_template("home.html", name = fname)
        else:
            cursor.close()
            conn.close()
            flash('Invalid username or password. Please try again.', 'error')
            return render_template("capstoneHome.html")
        
        
    else:
        flash('Eerror connecting to database', 'error')
        return render_template("capstoneHome.html")
        
    # return render_template("login.html", form=form)

@app.route('/selection')
def selection():
    return render_template("produceGrader1.html")



def get_uploaded_images():
    upload_folder = app.config['UPLOAD_FOLDER']
    uploaded_images = []

    if not os.path.exists(upload_folder):
        flash("File not found. Your uploads folder may have been removed")
    print(upload_folder)
    
    for filename in os.listdir(upload_folder):
        # Check if the path is a file (not a directory)
            if os.path.isfile(os.path.join(upload_folder, filename)):
                if filename.endswith(('.jpg', '.png')):
                    uploaded_images.append(filename)
    

    return uploaded_images


@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/files')
@login_required
def files():
    images_ = get_uploaded_images()
    return render_template('files.html', images=images_)




@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def connectToDB():
    connection = mysql.connector.connect(
    host="localhost",
    user="agrirate",
    password="password",
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