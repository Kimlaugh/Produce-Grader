import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
import re
import os
import shutil
import classifcation_model
import Produce_Grading
import time


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

currentUser['user_id'] = 1

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



def on_configure(event):
    # Update scroll region to fit the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))

query = "SELECT StockID,name, date FROM stock WHERE UserID = %s"
conn = connectToDB()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (currentUser['user_id'],))
    # cursor.execute(query)
    stocks = cursor.fetchall()
    cursor.close()
    conn.close()


produceRecords = tk.Tk()
produceRecords.geometry("700x500")
produceRecords.title("Produce Records")

canvas = tk.Canvas(produceRecords)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(produceRecords, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

titleLabel = tk.Label(inner_frame, text="My Produce Records")
titleLabel.config(font=("Arial", 14), fg="#BF3100")
titleLabel.pack()

recordCanvas = tk.Canvas(inner_frame, width=670, bg="#ffffff")
recordCanvas.pack()

# Display records
for idx, item in enumerate(stocks*9):
    stock_id = int(item["StockID"])
    name = item["name"]
    date_ = item["date"]

    recordCanvas.create_text(30, 15 + idx * 70, anchor='nw', text=f"Name: {name}", font=("Arial", 14))
    recordCanvas.create_text(30, 35 + idx * 70, anchor='nw', text=f"Date: {date_}", font=("Arial", 10))

    edit_button = tk.Button(inner_frame, text="Edit", command=lambda idx=stock_id: edit_item(idx))
    edit_button.place(x=450, y=20 + idx * 70)

    delete_button = tk.Button(inner_frame, text="Delete", command=lambda idx=stock_id: delete_item(idx))
    delete_button.place(x=520, y=20 + idx * 70)

inner_frame.bind("<Configure>", on_configure)

produceRecords.mainloop()
