import importlib
from tkinter import *
from tkinter import messagebox
import os
# Check if the 'data' directory exists before application start
if not os.path.exists('data'):
    os.makedirs('data')
# Check if the 'credentials.py' file exists before application start
if not os.path.isfile('data/credentials.py'):
    # If it doesn't exist, create it with default values
    with open('data/credentials.py', 'w', encoding='utf8') as outfile:
        outfile.write('email = "your_default_email"\n')
        outfile.write('password = "your_default_password"\n')

from data import credentials
from data import config as config
from pages.search_page import SearchPage
from modules.base import get_data
from modules.login import login
from warnings import simplefilter
from modules.tools import ToolManager


class Application:
    def __init__(self) -> None:
        self.white = '#FFFFFF'
        self.text_blue = '#01649b'
        self.tool_manager = ToolManager()
        self.clear_login_btn_img = None
        self.save_login_btn_img = None
        self.connect_btn_img = None
        self.clear_params_btn_img = None
        self.save_params_btn_img = None
        self.login_entry = None
        self.pwd_entry = None
        self.job_title_entry = None
        self.company_entry = None
        self.console_output = None


    def clear_cred(self) -> None:
        """
        Remove any text in the login and password text boxes (credentials)
        :return:            None
        """
        self.tool_manager.clear(self.login_entry)
        self.tool_manager.clear(self.pwd_entry)
        self.login_entry.focus()

    def clear_params(self) -> None:
        """
        Remove any text in the job title and company text boxes (config)
        :return:            None
        """
        self.tool_manager.clear(self.job_title_entry)
        self.tool_manager.clear(self.company_entry)
        self.job_title_entry.focus()

    def empty_cred_field_check(self) -> bool:
        """
        Checking that credentials are in place and information entered by User
        :return:            False - one or all entries are empty
                            True - if entries not empty and represents user's input
        """
        login = self.tool_manager.get_value(self.login_entry)
        pwd = self.tool_manager.get_value(self.pwd_entry)
        
        if len(login) == 0 or len(pwd) == 0:
            messagebox.showinfo(title='Empty fields', message='Please, do not leave any fields empty')
            return False
        else:
            return True

    def empty_param_field_check(self) -> bool:
        """
        Checking that parameters are in place and information entered by User
        :return:            False - one or all entries are empty
                            True - if entries not empty and represents user's input
        """
        job_title = self.tool_manager.get_value(self.job_title_entry)
        search_list = self.tool_manager.get_value(self.company_entry)
        if len(job_title) == 0 or len(search_list) == 0:
            messagebox.showinfo(title='Empty fields', message='Please, do not leave any fields empty')
            return False
        else:
            return True

    def predefine_cred(self) -> None:
        """
        Check if data file with login and password exist and populating values at the application start.
        If file doesn't exist (first run) - returning None
        :return:            None
        """
        cred = self.tool_manager.get_cred()
        if len(cred['email']) == 0 and len(cred['password']) == 0:
            self.login_entry.insert(0, 'your_default_email')
            self.pwd_entry.insert(0, 'your_default_password')
        else:
            self.login_entry.insert(0, cred['email'])
            self.pwd_entry.insert(0, cred['password'])

    def predefine_params(self) -> None:
        """
        Check if data file with job title and company exist and populating values at the application start.
        If file doesn't exist (first run) - returning None
        :return:            None
        """
        data = self.tool_manager.get_params()
        if len(data['search_list']) == 0 and len(data['job_titles']) == 0:
            self.company_entry.insert(0, 'name the company')
            self.job_title_entry.insert(0, 'name the position title')
        else:
            self.company_entry.insert(0, ', '.join(data['search_list']))
            self.job_title_entry.insert(0, ', '.join(data['job_titles']))

    def save_cred(self) -> None:
        """
        Save entered credential (login, password) to the configuration file for futrher use and
        reloading config file to make changes available during application session
        :return:            None
        """
        if self.empty_cred_field_check():
            data = self.tool_manager.prepare_cred(self.login_entry, self.pwd_entry)
            username = data['email']
            pwd = data['password']
            with open('data/credentials.py', 'w', encoding='utf8') as outfile:
                outfile.write(f'email = "{username}"\n')
                outfile.write(f'password = "{pwd}"\n')
        importlib.reload(credentials)

    def save_params(self) -> None:
        """
        Save entered parameters (job title, company) to the configuration file for futrher use and
        reloading config file to make changes available during application session
        :return:            None
        """
        if self.empty_param_field_check():
            data = self.tool_manager.prepare_param(self.job_title_entry, self.company_entry)
            company_list = data['search_list']
            job_titles = data['job_titles']

            # Read the entire config.py file
            with open('data/config.py', 'r', encoding='utf8') as infile:
                lines = infile.readlines()

            # Find the line that contains search_list and replace it
            for i, line in enumerate(lines):
                if line.strip().startswith('search_list'):
                    lines[i] = f'search_list = {company_list}\n'
                    break
            for i, line in enumerate(lines):
                if line.strip().startswith('job_titles'):
                    lines[i] = f'job_titles = {job_titles}\n'
                    break
                # break  # Stop searching once found

            # Write the modified lines back to config.py
            with open('data/config.py', 'w', encoding='utf8') as outfile:
                outfile.writelines(lines)
        importlib.reload(config)

    # ==================== Console operations ====================
    def update_console_output(self, text) -> None:
        """
        Updates console output every time console log got updated along application execution
        :param text:        Text from the console output, received from the search object
        :return:            None
        """
        self.console_output.config(state=NORMAL)  # Enable editing
        self.console_output.insert(END, text + '\n')  # Append text with a newline
        self.console_output.config(state=DISABLED)  # Disable editing
        self.console_output.update_idletasks()

    # ==================== Search operations ====================
    def sub_search(self):
        """
        Subscribe from search object ((c) Sergey Kolokolov) with minor integration tweaks
        """
        if self.empty_param_field_check() and self.empty_cred_field_check():
            self.save_cred()
            self.save_params()
            data = get_data()
            login(data)
            page = SearchPage(data)
            url = page.make_search_url(data["search_level"])
            page.open_url(url)
            for company in data["search_list"]:
                self.console_company = f'Searching for employees of {company}'
                print(self.console_company)
                self.update_console_output(self.console_company)
                page.search_company(company)
                search_pages_count = page.get_search_pages_count()
                print(f'Search returned {search_pages_count} pages of potential contacts within the {data["search_level"]} circle')
                self.update_console_output(f'Search returned {search_pages_count} pages of potential contacts within the {data["search_level"]} circle')
                invites_sent = 0
                for page_no in range(1, search_pages_count + 1):
                    if invites_sent == data["per_company_limit"]:
                        print(f'Already sent {invites_sent} invites to {company} employees which is maximum for one company')
                        self.update_console_output(f'Already sent {invites_sent} invites to {company} employees which is maximum for one company')
                        break
                    page.wait_all_people_loaded(page_no, search_pages_count)
                    invites_sent = page.send_invites(company, invites_sent, data, connection_level=2)
                    if data["connection_level"] == 3:
                        invites_sent = page.send_invites(company, invites_sent, data, connection_level=3)
                    page.go_to_next_search_page(search_pages_count)
            page.close_browser()
            simplefilter("ignore", ResourceWarning)

    # ==================== Building GUI ====================
    def create_entry(self) -> None:
        """
        Creates text boxed for user's input (tkinter Entry)
        :return:            None
        """
        # Creating text boxes
        self.login_entry = Entry(width=25, justify='left', fg=self.text_blue, highlightthickness=0)
        self.login_entry.grid(column=1, row=1)
        self.login_entry.focus()
        self.pwd_entry = Entry(width=25, justify='left', fg=self.text_blue, highlightthickness=0)
        self.pwd_entry.grid(column=1, row=2)
        self.job_title_entry = Entry(width=25, justify='left', fg=self.text_blue, highlightthickness=0)
        self.job_title_entry.grid(column=1, row=3)
        self.company_entry = Entry(width=25, justify='left', fg=self.text_blue, highlightthickness=0)
        self.company_entry.grid(column=1, row=4)

    def create_labels(self):
        """
        Creates text on the GUI window (tkinter labels)
        :return:            None
        """
        login_txt = Label(text='       Login', font=('Arial', 15), bg="white", fg=self.text_blue)
        login_txt.grid(column=0, row=1)
        pwd_txt = Label(text='Password', font=('Arial', 15), bg="white", fg=self.text_blue, anchor='e')
        pwd_txt.grid(column=0, row=2)
        job_title_txt = Label(text='   Job title', font=('Arial', 15), bg="white", fg=self.text_blue, anchor='e')
        job_title_txt.grid(column=0, row=3)
        company_txt = Label(text='Company', font=('Arial', 15), bg="white", fg=self.text_blue, anchor='e')
        company_txt.grid(column=0, row=4)
        hint_txt = Label(text='* Job title and Company could have multiple values, separated by comma.', font=('Arial', 10),
                        bg="white", fg=self.text_blue, anchor='e')
        hint_txt.grid(column=0, row=5, columnspan=2)

    def create_buttons(self):
        """
        Creates buttons and assign click events (tkinter Button)
        :return:            None
        """
        self.clear_login_btn_img = PhotoImage(file='data/img/clear_login_btn.png')
        clear_login_btn = Button(text='', borderwidth=0, border=0, image=self.clear_login_btn_img, highlightthickness=0,
                                command=self.clear_cred)
        clear_login_btn.grid(column=2, row=1)
        self.save_login_btn_img = PhotoImage(file='data/img/save_login_btn.png')
        save_login_btn = Button(text='', borderwidth=0, border=0, image=self.save_login_btn_img, highlightthickness=0,
                                command=self.save_cred)
        save_login_btn.grid(column=2, row=2)

        self.clear_params_btn_img = PhotoImage(file='data/img/clear_search_btn.png')
        clear_params_btn = Button(text='', borderwidth=0, border=0, image=self.clear_params_btn_img, highlightthickness=0,
                                command=self.clear_params)
        clear_params_btn.grid(column=2, row=3)

        self.save_params_btn_img = PhotoImage(file='data/img/save_search_btn.png')
        save_params_btn = Button(text='', borderwidth=0, border=0, image=self.save_params_btn_img, highlightthickness=0,
                                command=self.save_params)
        save_params_btn.grid(column=2, row=4)

        self.connect_btn_img = PhotoImage(file='data/img/extend_netw_btn.png')
        connect_btn = Button(text='', borderwidth=0, border=0, image=self.connect_btn_img, highlightthickness=0,
                            command=self.sub_search)
        connect_btn.grid(column=1, row=6)


    def create_window(self):
        """
        Build the whole GUI interface, including console output for user's convenient
        :return:            None
        """
        window = Tk()
        window.title('LinkedIn autoconnect')
        window.config(padx=5, pady=5, bg=self.white)
        window.geometry('510x800')
        window.resizable(False, False)

        canvas = Canvas(width=500, height=170)
        main_bg = PhotoImage(file='data/img/cropped_main_bg.png')
        canvas_image = canvas.create_image(248, 70, image=main_bg)
        canvas.config(bg=self.white, highlightthickness=0)
        canvas.grid(column=0, row=0, columnspan=3)

        # Create a Text widget for console output
        self.console_output = Text(window, width=70, height=35, wrap=WORD, state=DISABLED)
        self.console_output.grid(column=0, row=7, columnspan=3, pady=(10, 0))  # Adjust row and padding as needed


        self.create_labels()
        self.create_entry()
        self.create_buttons()

        self.predefine_cred()
        self.predefine_params()

        window.mainloop()

if __name__ == "__main__":
    program = Application()
    program.create_window()