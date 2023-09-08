from tkinter import *
import importlib
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data import credentials
from data import config as config

class ToolManager:
    """
    Class containing the objects that used from various objects to operate
    with data or entry fields, like prepare data to write, clear entries, 
    values from different entries and many more
    """
    def clear(self, entry) -> None:
        """
        Clear the texbox
        :param entry:               Location or name/variable of the textbox desired to be cleared
        :return:                    None
        """
        entry.delete(0, END)
            
    def get_value(self, entry) -> str:
        """
        Retrieving text from the texbox and returning its value as a string
        :param entry:               Location or name/variable of the textbox with user's input
        :return:                    String, representing user's input (text)
        """
        value = entry.get()
        return value
    
    def prepare_cred(self, login_entry, pwd_entry) -> dict:
        """
        Prepare data to write to configuration files
        :param login_entry:         Location or name/variable of the textbox
        :param pwd_entry:           Location or name/variable of the textbox
        :return:                    Dictionary, representing user's input (text) for configuration file
        """
        cred_to_write = {
            "email": self.get_value(login_entry),
            "password": self.get_value(pwd_entry)
        }
        return cred_to_write

    def prepare_param(self, job_title_entry, company_entry) -> dict:
        """
        Prepare data to write to configuration files
        :param login_entry:         Location or name/variable of the textbox
        :param pwd_entry:           Location or name/variable of the textbox
        :return:                    Dictionary, representing user's input (text) for configuration file
        """
        split_company = self.get_value(company_entry).split(', ')
        split_title = self.get_value(job_title_entry).split(', ')
        params_to_write = {
            "search_list": split_company,
            "job_titles":  split_title,
        }
        return params_to_write
    
    def get_cred(self):
        with open('data/credentials.py', 'r', encoding='utf8') as outfile:
            data = {
            "email": credentials.email,
            "password": credentials.password,
            }
        return data

    def get_params(self):
        with open('data/config.py', 'r', encoding='utf8') as outfile:
            data = {
            "search_list": config.search_list,
            "job_titles": config.job_titles,
            }
        return data
