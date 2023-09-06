from tkinter import *
from tkinter import messagebox
import os

# Check if the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')
# Check if the 'credentials.py' file exists
if not os.path.isfile('data/credentials.py'):
    # If it doesn't exist, create it with default values
    with open('data/credentials.py', 'w', encoding='utf8') as outfile:
        outfile.write('email = "your_default_email"\n')
        outfile.write('password = "your_default_password"\n')

from data import credentials
from data import config
# from modules.subscribe_from_search import sub_search

from pages.search_page import SearchPage
from modules.base import get_data
from modules.login import login
from warnings import simplefilter
# from main import update_console_output

# ==================== Variables ====================
white = '#FFFFFF'
text_blue = '#01649b'
clear_btn_img = None
save_btn_img = None
connect_btn_img = None
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
    # clear(job_title_entry)
    # clear(company_entry)
    login_entry.focus()

def clear_params() -> None:
    """
    Remove any text in the website and password text boxes
    :return:            None
    """
    clear(job_title_entry)
    clear(company_entry)
    job_title_entry.focus()

def get_value(entry) -> str:
    """
    Retrieving text from the texbox and returning its value as a string
    :param entry:               Location or name/variable of the textbox desired to be cleared
    :return:                    String, representing user's input (text)
    """
    value = entry.get()
    return value

def empty_cred_field_check():
    """
    Checking that all fields are filled with information and passing to the data saving
    :return:            None
    """
    login = get_value(login_entry)
    pwd = get_value(pwd_entry)
    # title = get_value(job_title_entry)
    # company = get_value(company_entry)

    # self.set_vars()
    if len(login) == 0 or len(pwd) == 0:
        messagebox.showinfo(title='Empty fields', message='Please, do not leave any fields empty')
        return False
    else:
        return True

def empty_param_field_check():
    """
    Checking that all fields are filled with information and passing to the data saving
    :return:            None
    """
    job_title = get_value(job_title_entry)
    search_list = get_value(company_entry)

    # self.set_vars()
    if len(job_title) == 0 or len(search_list) == 0:
        messagebox.showinfo(title='Empty fields', message='Please, do not leave any fields empty')
        return False
    else:
        return True


def get_cred():
    # try:
    with open('data/credentials.py', 'r', encoding='utf8') as outfile:
        data = {
        "email": credentials.email,
        "password": credentials.password,
        }
    return data
    # except FileNotFoundError:
    #     with open('data/credentials.py', 'w', encoding='utf8') as outfile:
    #         outfile.write('email = "your_default_email"\n')
    #         outfile.write('password = "your_default_password"\n')
    #         data = {
    #             "email": "your_default_email",
    #             "password": "your_default_password",
    #         }
    #         return data
    # finally:
    #     pass

def get_params():
    # try:
    with open('data/config.py', 'r', encoding='utf8') as outfile:
        data = {
        "search_list": config.search_list,
        "job_titles": config.job_titles,
        }
    return data
    # except FileNotFoundError:
    #     with open('data/config.py', 'w', encoding='utf8') as outfile:
    #         outfile.write('search_list = "[]"\n')
    #         outfile.write('job_titles = "[]"\n')
    #         data = {
    #             "search_list": [],
    #             "job_titles": [],
    #         }
    #         return data
    # finally:
    #     pass

def predefine_cred():
    global login_entry, pwd_entry
    """
    Check if data file with login and password exist and populating values at the application start.
    If file doesn't exist (first run) - returning None
    :return:            None
    """
    cred = get_cred()
    if len(cred['email']) == 0 and len(cred['password']) == 0:
        login_entry.insert(0, 'your_default_email')
        pwd_entry.insert(0, 'your_default_password')
    else:
        login_entry.insert(0, cred['email'])
        pwd_entry.insert(0, cred['password'])


def predefine_params():
    global job_title_entry, company_entry
    """
    Check if data file with login and password exist and populating values at the application start.
    If file doesn't exist (first run) - returning None
    :return:            None
    """
    data = get_params()
    if len(data['search_list']) == 0 and len(data['job_titles']) == 0:
        company_entry.insert(0, 'name the company')
        job_title_entry(0, 'name the position title')
    else:
        company_entry.insert(0, ', '.join(data['search_list']))
        job_title_entry.insert(0, ', '.join(data['job_titles']))

def prepare_cred():
    global login_entry, pwd_entry
    username = get_value(login_entry)
    pwd = get_value(pwd_entry)
    cred_to_write = {
        "email": username,
        "password": pwd
    }
    return cred_to_write

def prepare_param():
    global company_entry, job_title_entry
    company = get_value(company_entry)
    title = get_value(job_title_entry)
    split_company = company.split(', ')
    split_title = title.split(', ')
    params_to_write = {
        "search_list": split_company,
        "job_titles":  split_title,
    }
    return params_to_write

def save_cred():
    if empty_cred_field_check():
        data = prepare_cred()
        username = data['email']
        pwd = data['password']
        with open('data/credentials.py', 'w', encoding='utf8') as outfile:
            outfile.write(f'email = "{username}"\n')
            outfile.write(f'password = "{pwd}"\n')

def save_params():
    if empty_param_field_check():
        data = prepare_param()
        company_list = data['search_list']
        job_titles = data['job_titles']

        # Read the entire config.py file
        with open('data/config.py', 'r', encoding='utf8') as infile:
            lines = infile.readlines()

        # Find the line that contains search_list and replace it
        for i, line in enumerate(lines):
            if line.strip().startswith('search_list'):
                lines[i] = f'search_list = {company_list}\n'
            if line.strip().startswith('job_titles'):
                lines[i] = f'job_titles = {job_titles}\n'
            # break  # Stop searching once found

        # Write the modified lines back to config.py
        with open('data/config.py', 'w', encoding='utf8') as outfile:
            outfile.writelines(lines)

# ==================== Console operations ====================
def update_console_output(text):
    console_output.config(state=NORMAL)  # Enable editing
    console_output.insert(END, text + '\n')  # Append text with a newline
    console_output.config(state=DISABLED)  # Disable editing

# ==================== Search operations ====================
def sub_search():
    data = get_data()
    login(data)
    page = SearchPage(data)
    url = page.make_search_url(data["search_level"])
    page.open_url(url)
    for company in data["search_list"]:
        print(f'Searching for employees of {company}')
        update_console_output(f'Searching for employees of {company}')
        page.search_company(company)
        search_pages_count = page.get_search_pages_count()
        print(f'Search returned {search_pages_count} pages of potential contacts within the {data["search_level"]} circle')
        update_console_output(f'Search returned {search_pages_count} pages of potential contacts within the {data["search_level"]} circle')
        invites_sent = 0
        for page_no in range(1, search_pages_count + 1):
            if invites_sent == data["per_company_limit"]:
                print(f'Already sent {invites_sent} invites to {company} employees which is maximum for one company')
                update_console_output(f'Already sent {invites_sent} invites to {company} employees which is maximum for one company')
                break
            page.wait_all_people_loaded(page_no, search_pages_count)
            invites_sent = page.send_invites(company, invites_sent, data, connection_level=2)
            if data["connection_level"] == 3:
                invites_sent = page.send_invites(company, invites_sent, data, connection_level=3)
            page.go_to_next_search_page(search_pages_count)
    page.close_browser()
    simplefilter("ignore", ResourceWarning)

# ==================== Building GUI ====================
def create_entry():
    global login_entry, pwd_entry, job_title_entry, company_entry
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

def create_labels():
    login_txt = Label(text='       Login', font=('Arial', 15), bg="white", fg=text_blue)
    login_txt.grid(column=0, row=1)
    pwd_txt = Label(text='Password', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
    pwd_txt.grid(column=0, row=2)
    job_title_txt = Label(text='   Job title', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
    job_title_txt.grid(column=0, row=3)
    company_txt = Label(text='Company', font=('Arial', 15), bg="white", fg=text_blue, anchor='e')
    company_txt.grid(column=0, row=4)
    hint_txt = Label(text='* Job title and Company could have multiple values, separated by comma.', font=('Arial', 10),
                     bg="white", fg=text_blue, anchor='e')
    hint_txt.grid(column=0, row=5, columnspan=2)

def create_buttons():
    global clear_btn_img, save_btn_img, connect_btn_img
    clear_btn_img = PhotoImage(file='data/img/clear_btn_img.png')
    clear_login_btn = Button(text='', borderwidth=0, border=0, image=clear_btn_img, highlightthickness=0,
                             command=clear_cred)
    clear_login_btn.grid(column=2, row=1)
    save_btn_img = PhotoImage(file='data/img/save_btn_img.png')
    save_login_btn = Button(text='', borderwidth=0, border=0, image=save_btn_img, highlightthickness=0,
                            command=save_cred)
    save_login_btn.grid(column=2, row=2)

    clear_params_btn = Button(text='', borderwidth=0, border=0, image=clear_btn_img, highlightthickness=0,
                             command=clear_params)
    clear_params_btn.grid(column=2, row=3)
    save_params_btn = Button(text='', borderwidth=0, border=0, image=save_btn_img, highlightthickness=0,
                            command=save_params)
    save_params_btn.grid(column=2, row=4)

    connect_btn_img = PhotoImage(file='data/img/connect_btn_img.png')
    connect_btn = Button(text='', borderwidth=0, border=0, image=connect_btn_img, highlightthickness=0,
                         command=sub_search)
    connect_btn.grid(column=1, row=6)


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

# Create a Text widget for console output
console_output = Text(window, width=70, height=35, wrap=WORD, state=DISABLED)
console_output.grid(column=0, row=7, columnspan=3, pady=(10, 0))  # Adjust row and padding as needed


create_labels()
create_entry()
create_buttons()

predefine_cred()
predefine_params()

window.mainloop()
