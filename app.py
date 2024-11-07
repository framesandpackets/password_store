import tkinter as tk
from tkinter import messagebox, ttk
import db_scripts
import generate_pass
from cryptography.fernet import Fernet
import os


# generate encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key


# Function that either loads in your encrption key or creates one if it doesn't see a key
def load_key():
    if not os.path.exists("encryption_key.key"):
        return generate_key()
    else:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()


# loadings keys
key = load_key()
fernet = Fernet(key)


# Function to generate a password and set it in the password entry field (12 characters)
def generate_password():
    # You can pass the length of the password you want to create to the generate_pass function
    new_password = generate_pass.generate_pass(12)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, new_password)


# handle submission of a new entry
def submit_entry():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if service and username and password:
        password = fernet.encrypt(password.encode()).decode()
        db_scripts.create_entry(service, username, password)
        service_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        update_account_list()
        update_service_list()
    else:
        messagebox.showwarning("Warning!!", "Fill out all fields!")


# update the account list display
def update_account_list():
    account_list.delete(0, tk.END)
    display_accounts = db_scripts.get_all_enteries()
    for entry in display_accounts:
        password = fernet.decrypt(entry[3].encode()).decode()
        formatted_entry = f"Service: {entry[1]}  " + " " * 10 + f"   User: {entry[2]}      Password:   {password}    Password Last Updated:{entry[5]}"
        account_list.insert(tk.END, formatted_entry)


# update the dropdown with service names 
def update_service_list():
    services = [entry[1] for entry in db_scripts.get_all_enteries()]
    service_var.set('select a service in dropdown')  # Clear selection
    service_dropdown['values'] = services  # Update dropdown options


# password update for a selected service
def update_password():
    service_name = service_var.get()
    if service_name:
        new_password = generate_pass.generate_pass(12)
        encrypted_password = fernet.encrypt(new_password.encode()).decode()
        db_scripts.update_entry(encrypted_password, service_name)
        messagebox.showinfo("Success", f"Password for {service_name} has been updated.")
        update_account_list()
    else:
        messagebox.showwarning("Please select a service to update.")


# main window
root = tk.Tk()
root.title("Password Store")
root.geometry("1100x500")
root.configure(bg="#000000")

font_style = ("Helvetica", 12)

# parent frame for 'Add New Entry' and 'Update Password'
top_frame = tk.Frame(root, bg="#000000")
top_frame.pack(pady=10, padx=10)


# Frame for adding new entries
tk.Label(top_frame, text="Add New Entry", font=("Helvetica", 16, "bold"), fg="white", bg="#000000").grid(row=0, column=0, pady=10)
input_frame = tk.Frame(top_frame, bg="#000000")
input_frame.grid(row=1, column=0, padx=10, sticky="n")

# service name
tk.Label(input_frame, text="Service Name:", font=font_style, fg="white", bg="#000000").grid(row=0, column=0, sticky="e", padx=5, pady=5)
service_entry = tk.Entry(input_frame, width=25, font=font_style)
service_entry.grid(row=0, column=1, padx=5, pady=5)

# user
tk.Label(input_frame, text="Username:", font=font_style, fg="white", bg="#000000").grid(row=1, column=0, sticky="e", padx=5, pady=5)
username_entry = tk.Entry(input_frame, width=25, font=font_style)
username_entry.grid(row=1, column=1, padx=5, pady=5)

#pass
tk.Label(input_frame, text="Password:", font=font_style, fg="white", bg="#000000").grid(row=2, column=0, sticky="e", padx=5, pady=5)
password_entry = tk.Entry(input_frame, width=25, font=font_style)
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Generate Password Button...ugly buttons :(
generate_button = tk.Button(input_frame, text="Generate Password", font=font_style, fg="white", command=generate_password, bg="#000000", borderwidth=2, highlightthickness=2)
generate_button.grid(row=2, column=2, padx=5, pady=5)

# submit Button
submit_button = tk.Button(input_frame, text="Submit", font=font_style, fg="white", bg="#000000", command=submit_entry, highlightbackground="white", highlightthickness=2, borderwidth=2)
submit_button.grid(row=3, column=0, columnspan=3, pady=10)

# frame for updating existing passwords, next to input_frame
tk.Label(top_frame, text="Update Password", font=("Helvetica", 16, "bold"), fg="white", bg="#000000").grid(row=0, column=1, pady=10)
update_frame = tk.Frame(top_frame, bg="#000000")
update_frame.grid(row=1, column=1, padx=20, sticky="n")

# Dropdown for selecting service to update
service_var = tk.StringVar()
service_dropdown = ttk.Combobox(update_frame, textvariable=service_var, font=font_style, width=22)
service_dropdown.pack(pady=5)

# Update Password Button
update_button = tk.Button(update_frame, text="Update Service Password", font=font_style, fg="white", bg="#000000", command=update_password, borderwidth=2, highlightbackground="white", highlightthickness=2)
update_button.pack(pady=10)

# Display area for accounts below the Add New Entry and Update Password frames
tk.Label(root, text="My Accounts", font=("Helvetica", 15), fg="white", bg="#000000").pack(pady=10)
account_list = tk.Listbox(root, width=100, height=40, font=("Helvetica", 12), fg="white", bg="#000000")
account_list.pack()



# Load initial account entries and service list
update_account_list()
update_service_list()

root.mainloop()
