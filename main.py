from tkinter import *
from tkinter import messagebox

# ==================== Variables ====================
white = '#FFFFFF'
text_blue = '#01649b'

# ==================== Data operations ====================
def clear(entry) -> None:
    """
    Clear the texbox
    :param entry:               Location or name/variable of the textbox desired to be cleared
    :return:                    None
    """
    entry.delete(0, END)

def clear_cred() -> None:
    """
    Remove any text in the website and password text boxes
    :return:            None
    """
    clear(login_entry)
    clear(pwd_entry)
    clear(job_title_entry)
    clear(company_entry)

    login_entry.focus()

def get_value(entry) -> str:
    """
    Retrieving text from the texbox and returning its value as a string
    :param entry:               Location or name/variable of the textbox desired to be cleared
    :return:                    String, representing user's input (text)
    """
    value = entry.get()
    return value
def empty_field_check() -> bool:
    """
    Checking that all fields are filled with information and passing to the data saving
    :return:            None
    """
    login = get_value(login_entry)
    pwd = get_value(pwd_entry)
    title = get_value(job_title_entry)
    company = get_value(company_entry)

    # self.set_vars()
    if len(login) == 0 or len(pwd) == 0 or len(title) == 0 or len(company) == 0:
        messagebox.showinfo(title='Empty fields', message='Please, do not leave any fields empty')
    else:
        return True

def predefine_cred():
    """
    Check if data file with login and password exist and populating values at the application start.
    If file doesn't exist (first run) - returning None
    :return:            None
    """
    # self.set_vars()
    try:
        with open('data/credentials.py', 'r', encoding='utf8') as outfile:
            # read data from file in format:
    # email = "value"
    # password = "value"
            # data = json.load(outfile)
    except FileNotFoundError:
        messagebox.showinfo(title='No file found', message='Looks like you are running this program first time. \n'
                                                           'Data with password records not found')
    else:
        if self.website in data:
            username = data[self.website]['username']
            password = data[self.website]['password']
            messagebox.showinfo(title=self.website, message=f'Email: {username}\nPassword: {password}')
        else:
            messagebox.showinfo(title='No data found', message=f'No data for {self.website} exist.')
# ==================== Console operations ====================

# ==================== Building GUI ====================
# def flip_background():


window = Tk()
window.title('LinkedIn autoconnect')
window.config(padx=5, pady=5, bg=white)
window.geometry('510x800')
window.resizable(False, False)

canvas = Canvas(width=500, height=170)
main_bg = PhotoImage(file='data/img/cropped_main_bg.png')
canvas_image = canvas.create_image(248, 70, image=main_bg)
canvas.config(bg=white, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

# Creating text (labels)
login_txt = Label(text='       Login', font=('Arial', 15), bg="white", fg=text_blue)
login_txt.grid(column=0, row=1)
pwd_txt = Label(text='Password', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
pwd_txt.grid(column=0, row=2)
job_title_txt = Label(text='   Job title', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
job_title_txt.grid(column=0, row=3)
company_txt = Label(text='Company', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
company_txt.grid(column=0, row=4)
hint_txt = Label(text='* Job title and Company could have multiple values, separated by comma.', font=('Arial', 10), bg="white", fg=text_blue, anchor='e')
hint_txt.grid(column=0, row=5, columnspan=2)

# Creating text boxes
login_entry = Entry(width=25, justify='left', fg=text_blue, highlightthickness=0)
login_entry.grid(column=1, row=1)
login_entry.focus()
pwd_entry = Entry(width=25, justify='left', fg=text_blue, highlightthickness=0)
pwd_entry.grid(column=1, row=2)
job_title_entry = Entry(width=25, justify='left', fg=text_blue, highlightthickness=0)
job_title_entry.grid(column=1, row=3)
company_entry = Entry(width=25, justify='left', fg=text_blue, highlightthickness=0)
company_entry.grid(column=1, row=4)


# Creating buttons
clear_btn_img=PhotoImage(file='data/img/clear_btn_img.png')
clear_login_btn = Button(text='', borderwidth=0, border=0, image=clear_btn_img, highlightthickness=0, command=clear_cred)
clear_login_btn.grid(column=2, row=3)
save_btn_img=PhotoImage(file='data/img/save_btn_img.png')
save_login_btn = Button(text='', borderwidth=0, border=0, image=save_btn_img, highlightthickness=0, command=clear_cred)
save_login_btn.grid(column=2, row=4)
connect_btn_img=PhotoImage(file='data/img/connect_btn_img.png')
connect_btn = Button(text='', borderwidth=0, border=0, image=connect_btn_img, highlightthickness=0, command=clear_cred)
connect_btn.grid(column=1, row=6)



window.mainloop()
