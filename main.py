from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.option_add('*Dialog.msg.font', 'Helvetica 12')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_block.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Copied", message="Your random password is copied!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_block.get()
    email = email_username_block.get()
    password = password_block.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any field empty.")
    else:
        #test if it is successfully executed(only in case that data.json exists)
        try:
            with open("data.json", 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        #if FileNotFoundError occurs, creat a data file with new_data
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        #if it is executed without problems, update and write
        else:
            data.update(new_data)

            with open("data.json", 'w') as data_file:
                json.dump(data, data_file, indent=4)
        #no matter what, this will be executed
        finally:    
            website_block.delete(0, END)
            #email_username_block.delete(0, END)
            password_block.delete(0, END)
            messagebox.showinfo(title="Added", message="Your information is successfully stored.")
            website_block.focus()


def find_password():
    website = website_block.get()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No Data File Found", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: \n{email} \n\nPassword: \n{password}")
        else:
            if len(website) == 0:
                messagebox.showinfo(title="Error", message="No details for this exists.")
            else:    
                messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

        


# ---------------------------- UI SETUP ------------------------------- #



canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(130,100, image=logo_img)
canvas.grid(column=1,row=0)


#Labels
website = Label(text="Website:")
website.grid(column=0,row=1)

email_username = Label(text="Email/Username:")
email_username.grid(column=0,row=2)

password = Label(text="Password:")
password.grid(column=0,row=3)


#Entries
website_block = Entry(width=21)
website_block.grid(column=1,row=1)
website_block.focus()

email_username_block = Entry(width=41)
email_username_block.grid(column=1, row=2, columnspan=2)
email_username_block.insert(0, "jaehan.kim@studmail.w-hs.de")

password_block = Entry(width=21)
password_block.grid(column=1,row=3)

#Buttons
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(column=2,row=3)

search_button = Button(text="Search", width=16, command=find_password)
search_button.grid(column=2,row=1)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1,row=4, columnspan=2)




window.mainloop()