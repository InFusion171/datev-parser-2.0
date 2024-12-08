import os
from tkinter import messagebox
from Transaction import sort_by_buchungstag

class FileCreation:
    @staticmethod
    def create_files(transaction_by_date: dict, account_owner: str, output_path: str):
        DIRECTORY_PATH = f'{output_path}/{account_owner} Bankumsätze'

        if os.path.exists(DIRECTORY_PATH):
            #messagebox.showerror('Error', f'Ordner "{DIRECTORY_PATH}" existiert bereits') 
            return False, DIRECTORY_PATH
        
        os.makedirs(DIRECTORY_PATH)

        for valuta, transactions in transaction_by_date.items():
            with open(f'{DIRECTORY_PATH}/{valuta} Sparda-Bankumsätze.txt', 'w+') as f:
                for transaction in sort_by_buchungstag(transactions):
                    f.write(f'{transaction.create_datev_format()}\n')

        return True, ''
        #messagebox.showinfo('Erfolgreich', f'Bankumsätze von {account_owner} in "{output_path}" erstellt')