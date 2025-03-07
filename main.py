from tkinter import *
from tkinter import messagebox
from queue import Queue
import pystray
from tkcalendar import DateEntry
from datetime import *
from dateutil import relativedelta
import json
from plyer import notification
from PIL import Image
from threading import Thread
import os
import sys
import winreg as reg
import ctypes
# ---------------------------- TRAY ICON FUNCTIONALITY ------------------------------- #
ctypes.windll.kernel32.SetConsoleTitleW("Gym Subscription Manager")
image = Image.open("Files/xD.png")
task_queue = Queue()
# def on_minimize(event):
#     print("Window minimized")
#     # Hide the window or perform any other action here if needed
#     # root.withdraw()
#
# Function to handle window close event
def on_close():
    window.withdraw()

def restore_window():
    window.deiconify()

def open_new_window():
    task_queue.put(lambda: search())

def process_queue():
    while not task_queue.empty():
        task = task_queue.get()
        task()
    window.after(100, process_queue)

def after_click(icon, query):
    if str(query) == "Open":
        restore_window()
        # icon.stop()
    elif str(query) == "Search":
        open_new_window()
        window.after(100, process_queue)
        # icon.stop()
    elif str(query) == "Exit":
        icon.stop()
        window.quit()

def setup_tray_icon():
    icon = pystray.Icon("Menu", image, "Client Subscription Manager", menu=pystray.Menu(
            pystray.MenuItem("Open", lambda: after_click(icon, "Open")),
            pystray.MenuItem("Search", lambda: after_click(icon, "Search")),
            pystray.MenuItem("Exit", lambda: after_click(icon, "Exit"))
        ),
    )
    icon.run()
# ---------------------------- START UP LOGIC ------------------------------- #
def add_to_startup(app_name, app_path=None):
    """
    Add the application to Windows startup.

    :param app_name: Name of the application (key in the registry).
    :param app_path: Full path to the application executable.
                     Defaults to the current script path.
    """
    try:
        # Default to the current script if no path is provided
        if app_path is None:
            app_path = os.path.abspath(sys.argv[0])

        # Access the registry key
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)

        # Add the registry entry
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, app_path)
        reg.CloseKey(reg_key)
        # messagebox.showinfo(title="Oops", message=f"Added {app_name} to startup successfully.")

    except Exception as e:
        messagebox.showinfo(title="Oops", message=f"Failed to add {app_name} to startup: {e}")
# ---------------------------- VARIABLES ------------------------------- #
now = date.today()
current_day_next_month = now + relativedelta.relativedelta(months=1)
today = now.strftime("%m/%d/%y")
month = int(current_day_next_month.strftime("%m"))
# ---------------------------- CREDENTIALS SEARCHER ------------------------------- #
def search():
    second_window = Tk()
    second_window.title("Client Subscriptions")

    # Create a Canvas for scrolling
    second_canvas = Canvas(second_window)
    second_canvas.grid(row=0, column=0, sticky="nsew")

    # Add a Scrollbar and link it to the canvas
    scrollbar = Scrollbar(second_window, orient=VERTICAL, command=second_canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure canvas to work with scrollbar
    second_canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the labels
    scrollable_frame = Frame(second_canvas)

    # Add the scrollable frame to the canvas
    second_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Populate the frame with data from the JSON file
    num_1 = 0
    with open("Files/user_data.json", mode="r") as data:
        data_xd = json.load(data)
        for x in data_xd:
            # Create labels inside the scrollable frame
            label_name = Label(scrollable_frame, text=data_xd[x]['name'])
            label_date = Label(scrollable_frame, text="Valid until: " + data_xd[x]['date'])
            label_name.grid(column=0, row=num_1, padx=10, pady=5)
            label_date.grid(column=1, row=num_1, padx=10, pady=5)
            num_1 += 1

    # Update the scroll region to accommodate the size of the content
    scrollable_frame.update_idletasks()
    second_canvas.config(scrollregion=second_canvas.bbox("all"))

    # Mouse scroll event bindings
    def on_mouse_scroll(event):
        if event.delta:  # For Windows
            second_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num == 4:  # For Linux/macOS: Scroll up
            second_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # For Linux/macOS: Scroll down
            second_canvas.yview_scroll(1, "units")

    # Bind the scroll event to the canvas
    if second_window.tk.call("tk", "windowingsystem") == "win32":
        second_canvas.bind_all("<MouseWheel>", on_mouse_scroll)
    else:
        second_canvas.bind_all("<Button-4>", on_mouse_scroll)  # Scroll up
        second_canvas.bind_all("<Button-5>", on_mouse_scroll)  # Scroll down
# ---------------------------- CHECK IF SUBSCRIPTION IS STILL VALID/NOTIFICATIONS ------------------------------- #
def compare_dates():
    try:
        with open("Files/user_data.json", mode="r") as data:
            # Reading old data
            data_xd = json.load(data)

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("Files/user_data.json", mode="w") as data:
            pass
    else:
        for x in data_xd:
            if str(today) == str(data_xd[x]['date']):
                notification.notify(
                    title='Subscription Expired',
                    message=f"{data_xd[x]['name']}'s Subscription has Expired",
                    app_icon="Files/gym_icon.ico",
                    app_name="Gym Subscription Manager",
                    timeout=15,
                )

def schedule_comparison():
   compare_dates()  # Call the function
   window.after(86400000 , schedule_comparison)
# ---------------------------- SAVER ------------------------------- #
def save(*args):
    name = name_entry.get()
    date_e = date_entry.get()
    new_data = {
           name :{
               "name": name,
               "date": date_e
           }
    }
    if len(name) ==0 or len(date_e) == 0:
        messagebox.showinfo(title = "Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("Files/user_data.json", mode ="r") as data:
                # Reading old data
                data_xd =json.load(data)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("Files/user_data.json", mode="w") as data:
                json.dump(new_data, data, indent=4)
        else:
            data_xd.update(new_data)
            with open("Files/user_data.json", mode="w") as data:
                json.dump(data_xd, data, indent = 4)
        finally:
            name_entry.delete(0, END)
# --------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Client Subscription Manager")

canvas = Canvas(width=400, height=240 )
logo = PhotoImage(file ="Files/xD.png")
# notifications_icon = PhotoImage(file="logo.png")
canvas.create_image(200,120, image = logo)
canvas.grid(column = 1, row = 0, padx = 50, pady = 50 )

# Labels
name_label = Label(text = "Name:")
name_label.grid(column = 0, row = 1, sticky="w")

date_label = Label(text = "Valid until:")
date_label.grid(column = 0, row = 2, sticky="w")

# Entries
name_entry = Entry(width = 30)
name_entry.grid(column=1, row=1, sticky="w", pady=10)
name_entry.focus_set()

date_entry = DateEntry( month=month, width=27)
date_entry.grid(column = 1, row =2, sticky="w")

#Bind both Entries to "Enter"
name_entry.bind("<Return>", save)
date_entry.bind("<Return>", save)

# Buttons
add_button = Button(text = "Add", width = 14, command=save)
add_button.grid(column = 1, row =3)
add_button.place(x=315, y=409)

search_button = Button(text = "Search", width=14, command=search)
search_button.grid(column = 1, row =3, sticky="e", pady=5, padx=5)

window.protocol("WM_DELETE_WINDOW", on_close)
tray_thread = Thread(target=setup_tray_icon, daemon=True)
tray_thread.start()
schedule_comparison()
add_to_startup("Client Subscription Manager")
window.mainloop()
