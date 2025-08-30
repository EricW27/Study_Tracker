'''
STUDY TRACKER BETA
Author: Eric Wing

Settings Tab

'''

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QMessageBox)

class SubjectsTab(QWidget):
    def __init__(self, tracker, today_tab, history_tab):
        super().__init__()
        self.tracker = tracker
        self.today_tab = today_tab
        self.history_tab = history_tab

        layout = QVBoxLayout()

        self.subject_list = QListWidget()
        self.subject_list.addItems(self.tracker.subjects)
        layout.addWidget(self.subject_list)

        #Add subject controls
        add_layout = QHBoxLayout()
        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("New subject name")
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_subject)
        add_layout.addWidget(self.add_input)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)

        #Rename controls
        rename_layout = QHBoxLayout()
        self.rename_input = QLineEdit()
        self.rename_input.setPlaceholderText("Rename selected subject")
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self.rename_subject)
        rename_layout.addWidget(self.rename_input)
        rename_layout.addWidget(self.rename_btn)
        layout.addLayout(rename_layout)

        #Delete controls
        delete_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_subject)
        delete_layout.addWidget(self.delete_btn)
        layout.addLayout(delete_layout)

        #Clear History controls
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_btn)

        self.setLayout(layout)

    #Updates data on UI
    def refresh_list(self):
        self.subject_list.clear()
        self.subject_list.addItems(self.tracker.subjects)
        self.today_tab.subject_box.clear()
        self.today_tab.subject_box.addItems(self.tracker.subjects)
        self.today_tab.update_table()
        self.history_tab.update_table()

    def add_subject(self):
        name = self.add_input.text().strip()
        if not name:
            return
        self.tracker.add_subject(name)
        self.add_input.clear()
        self.refresh_list()

    def rename_subject(self):
        selected = self.subject_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a subject to rename.")
            return
        old_name = selected.text()
        new_name = self.rename_input.text().strip()
        if not new_name:
            return
        self.tracker.rename_subject(old_name, new_name)
        self.rename_input.clear()
        self.refresh_list()

    def delete_subject(self):
        selected = self.subject_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a subject to delete.")
            return
        
        subject_name = selected.text()
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{subject_name}'? This will also remove its history.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.tracker.delete_subject(subject_name)
            self.refresh_list()

    def clear_history(self):
        
        confirm = QMessageBox.question(
            self,
            "Confirm Reset",
            f"Are you sure you want to clear history? This will delete all subjects and time logs.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:

            confirm_d = QMessageBox.question(
                self,
                "Confirm Confirm",
                f"Are you REALLY sure you want to clear history? This will delete EVERYTHING.",
                QMessageBox.No | QMessageBox.Yes,
            )
            if confirm_d == QMessageBox.Yes:
                import os

                #Delete save file
                if os.path.exists(self.tracker.save_file):
                    os.remove(self.tracker.save_file)
                
                #Reset everything
                self.tracker.__init__(self.tracker.save_file)

                #Update subjects list in the tab
                self.refresh_list()

                if hasattr(self.parent(), 'history_tab'):
                    self.parent().history_tab.update_table()