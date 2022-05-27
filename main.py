from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


def password_generator():
    """Password Generator"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def find_data():
    """Find Data"""
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found. ")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


def save_data():
    """Save Data"""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }
    if website and email and password:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered\nEmail: {website}\n\
        Password: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
    else:
        messagebox.showinfo("Oops", "Please make sure you haven't left any fields empty")


# Window
window = Tk()
window.title("Password Manager")
window.resizable(width=False, height=False)
window.config(padx=50, pady=50)
logo_img = PhotoImage(file="logo.png")

# Canvas
canvas = Canvas(width=200, height=190, highlightthickness=0)
canvas.create_image(100, 95, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=20)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=20)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=11, command=find_data)
search_button.grid(row=1, column=2)
generate_psw_button = Button(text="Generate Password", width=11, command=password_generator)
generate_psw_button.grid(row=3, column=2)
add_button = Button(text="Add", width=33, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()
