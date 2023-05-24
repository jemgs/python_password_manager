from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password_entry.delete(0, END)
    nr_letters = random.randint(6, 7)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ----------------------------   SAVE PASSWORD ------------------------------- #
def save_password():
    web = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        web: {
            "email": email,
            "password": password
        }
    }
    # To show the inputted info to the user:
    if web == "" or email == "" or password == "":
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty")
    else:
        try:
            with open("passwords.json", "r") as f:
                # Reading old data:
                data = json.load(f)  # This store a type dictionary var of the json dile.
        except FileNotFoundError:
            with open("passwords.json", "w") as f:
                # Saving updated data:
                json.dump(new_data, f, indent=4)  # This is to write data and creating a json file of a dict.
        else:
            # Updating old data with new data:
            data.update(new_data)
            with open("passwords.json", "w") as f:
                # Saving updated data:
                json.dump(data, f, indent=4)  # This is to write data and creating a json file of a dict.

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.focus()


# ---------------------------- PASSWORD SEARCH ------------------------------- #

def search_password():
    web = website_entry.get()
    try:
        with open("passwords.json", "r") as f:
            # Reading old data:
            data = json.load(f)  # This store a type dictionary var of the json dile.
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="There is no saved data")
    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo(title=web, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="This page is not registered")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("password manager")
window.minsize(width=350, height=350)
window.config(padx=20, pady=20)

logo = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
logo.create_image(100, 100, image=logo_image)
logo.grid(column=1, row=0)

website_Label = Label()
website_Label.config(text="Website")
website_Label.grid(column=0, row=1)

email_Label = Label()
email_Label.config(text="Email/Username: ")
email_Label.grid(column=0, row=2)

password_label = Label()
password_label.config(text="Password")
password_label.grid(column=0, row=3)

# Columnspan property is for determining how many columns will an object ocupy:
# Sticky property to define the widget alignment:
# N: stick to the top edge
# S: stick to the bottom edge
# W: stick to the left edge
# E: stick to the right edge
# NW: stick to the top-left corner
# NE: stick to the top-right corner
# SW: stick to the bottom-left corner
# SE: stick to the bottom-right corner
# CENTER: center the widget within the cell

website_entry = Entry()
website_entry.config(width=19)
website_entry.focus()
website_entry.grid(column=1, row=1, sticky=W)

email_entry = Entry()
email_entry.config(width=34)
email_entry.insert(0, "youremail@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2, sticky=W)

password_entry = Entry()
password_entry.config(width=19)
password_entry.grid(column=1, row=3, sticky=W)

search_button = Button()
search_button.config(text="Search", width=11, command=search_password)
search_button.grid(column=1, row=1, sticky=E)

generate_pass_button = Button()
generate_pass_button.config(text="Generate", width=11, command=password_generator)
generate_pass_button.grid(column=1, row=3, sticky=E)

add_button = Button()
add_button.config(text="Add", width=28, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky=W)

window.mainloop()
