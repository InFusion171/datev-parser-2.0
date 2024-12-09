import os
import re
import sys
import chardet
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QFormLayout, QWidget, 
    QFrame, QMessageBox, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from FileCreation import FileCreation
from Transaction import Transaction

class Gui(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(500, 300)

        #self.setMinimumSize(400, 300)
        #self.setMaximumSize(800, 600)

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet(u'QLabel#account_owner {padding-top: 15px;padding-bottom: 15px;}')

        # Font for consistent styling
        font = QFont('Arial', 12)

        self.account_owner_label = QLabel('')
        self.account_owner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.account_owner_label.setObjectName('account_owner')
        self.account_owner_label.setFont(QFont('Arial', 16, 5))

        self.account_owner_label.setHidden(True)

        main_layout.addWidget(self.account_owner_label)

        # Form Layout for IBAN and BIC
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # IBAN Input
        self.iban_input = QLineEdit()
        self.iban_input.setFont(font)
        iban_label = QLabel('IBAN')
        iban_label.setFont(font)
        form_layout.addRow(iban_label, self.iban_input)

        # BIC Input
        self.bic_input = QLineEdit()
        self.bic_input.setFont(font)
        bic_label = QLabel('BIC')
        bic_label.setFont(font)
        form_layout.addRow(bic_label, self.bic_input)

        main_layout.addLayout(form_layout)

        main_layout.addStretch()

        # File Selection Button
        file_button_layout = QHBoxLayout()
        self.pick_file_button = QPushButton('Datei auswählen')
        self.pick_file_button.setFont(font)
        self.pick_file_button.clicked.connect(self.select_file)
        self.pick_file_button.clicked.connect(self.update_account_owner_label)

        file_button_layout.addWidget(self.pick_file_button)
        main_layout.addLayout(file_button_layout)

        # Output Directory Selection Button
        output_button_layout = QHBoxLayout()
        self.pick_output_dir_button = QPushButton('Ausgabepfad auswählen')
        self.pick_output_dir_button.setFont(font)
        self.pick_output_dir_button.clicked.connect(self.select_output_directory)
        output_button_layout.addWidget(self.pick_output_dir_button)
        main_layout.addLayout(output_button_layout)

        main_layout.addStretch()

        # Generate Button
        generate_button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Generieren')
        self.generate_button.setFont(font)
        self.generate_button.clicked.connect(self.generate)
        generate_button_layout.addWidget(self.generate_button)
        main_layout.addLayout(generate_button_layout)

        # Additional instance variables
        self.account_owner = ''
        self.content = ''
        self.output_path = ''
        self.selected_filename = ''

    def run(self):
        self.show()

    def get_account_owner(self, file_content: str):
        account_owner = re.search('"Kontoinhaber:";"(.*)"\n', file_content).group(1)

        if account_owner:
            return account_owner
        
        return ''

    def update_account_owner_label(self):
        account_owner = self.get_account_owner(self.content)

        if account_owner:
            self.account_owner_label.setText('Kontoinhaber: ' + account_owner)
            self.account_owner_label.setHidden(False)

    def generate(self):
        if len(self.content) == 0:
            QMessageBox.critical(self, "Error", "Zuerst eine Datei auswählen")
            return

        if len(self.iban_input.text()) == 0:
            QMessageBox.critical(self, "Error", "IBAN Feld ist leer")
            return

        if len(self.bic_input.text()) == 0:
            QMessageBox.critical(self, "Error", "BIC Feld ist leer")
            return

        if len(self.output_path) == 0:
            QMessageBox.critical(self, "Error", "Bitte den Zielpfad auswählen")
            return

        try:
            self.account_owner, self.transaction_by_date = Transaction.parse(
                self.iban_input.text(), 
                self.bic_input.text(), 
                self.content
            )

        except AttributeError:
            QMessageBox.critical(self, "Error", "Zuerst eine Datei auswählen")
            return
        except Exception:
            QMessageBox.critical(self, "Error", "Das Format der Datei stimmt nicht")
            return

        created_files, directory_path = FileCreation.create_files(self.transaction_by_date, self.account_owner, self.output_path)

        if created_files:
            QMessageBox.information(self, 'Erfolgreich', f'Bankumsätze von {self.account_owner} in "{self.output_path}" erstellt')
            self.iban_input.setText('')
            self.bic_input.setText('')
            self.pick_file_button.setText('Datei auswählen')
            self.selected_filename = ''

            self.pick_output_dir_button.setText('Ausgabepfad wählen')
            self.output_path = ''

            self.account_owner_label.setHidden(True)

        else:
            QMessageBox.critical(self, 'Error', f'Ordner "{directory_path}" existiert bereits')


    def select_output_directory(self):
        path = QFileDialog.getExistingDirectory(self, 'Zielpfad auswählen')

        if path:
            self.output_path = path
        
            # Split the path and get the last 3 subdirectories
            path_parts = path.split(os.path.sep)
            
            # If there are fewer than 3 parts, show the full path or last part
            if len(path_parts) < 3:
                shortened_path = path_parts[-1] if path_parts else path
            else:
                # Take the last 3 parts and join them
                shortened_path = os.path.join(*path_parts[-3:])
            
            # Limit total length if needed
            if len(shortened_path) > 30:
                shortened_path = '...' + shortened_path[-27:]
            
            self.pick_output_dir_button.setText('Ausgabepfad: ' + shortened_path)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            'Datei auswählen',
            filter='Spardabank Überweisungs export (*.csv *.txt)'
        )

        if not path:
            return

        filename = os.path.basename(path)
        
        #Shorten filename if it's too long
        if len(filename) > 40:
            filename = filename[:37] + '...'
        
        self.pick_file_button.setText('Datei: ' + filename)

        with open(path, 'rb') as file:
            raw_data = file.read()

        result = chardet.detect(raw_data)
        encoding = result['encoding']

        if encoding is None:
            QMessageBox.critical(self, "Error", "Das Encoding der Datei konnte nicht erkannt werden")
            return

        self.content = raw_data.decode(encoding)
        self.selected_filename = path

def main():
    app = QApplication(sys.argv)
    gui = Gui("Spardabank Überweisungs export zu DATEV Format")
    gui.run()

    app.setStyle('Fusion')

    sys.exit(app.exec())

if __name__ == "__main__":
    main()