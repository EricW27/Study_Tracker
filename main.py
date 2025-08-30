'''
STUDY TRACKER BETA
Author: Eric Wing

Frontend Logic

'''

import os, sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget
)

from PySide6.QtGui import QIcon
from study_tracker import StudyTracker
from history import HistoryTab
from settings import SubjectsTab
from today import TodayTab

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)


class StudyTrackerApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Tracker")

        icon_path = resource_path("resources/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.tracker = StudyTracker()
        if not self.tracker.subjects:
            self.tracker.create_account(["Math", "Physics", "CS"])

        # Tabs
        tabs = QTabWidget()
        self.history_tab = HistoryTab(self.tracker)
        self.today_tab = TodayTab(self.tracker, self.history_tab)
        self.subjects_tab = SubjectsTab(self.tracker, self.today_tab, self.history_tab)

        tabs.addTab(self.today_tab, "Today")
        tabs.addTab(self.history_tab, "History")
        tabs.addTab(self.subjects_tab, "Settings")


        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyTrackerApp()
    window.show()
    sys.exit(app.exec())
