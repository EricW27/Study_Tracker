'''
STUDY TRACKER BETA
Author: Eric Wing

Today Tab

'''
import time

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import QTimer

class TodayTab(QWidget):
    def __init__(self, tracker, history_tab):
        super().__init__()
        self.tracker = tracker
        self.history_tab = history_tab

        self.timer_running = False
        self.start_time = None
        self.current_subject = None

        layout = QVBoxLayout()

        self.subject_box = QComboBox()
        self.subject_box.addItems(self.tracker.subjects)
        layout.addWidget(self.subject_box)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_timer)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_timer)
        layout.addWidget(self.stop_btn)

        self.timer_label = QLabel("00:00:00")
        layout.addWidget(self.timer_label)

        self.table = QTableWidget(len(self.tracker.subjects) + 1, 2)
        self.table.setHorizontalHeaderLabels(["Subject", "Time"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.update_table()

        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self.update_timer)

    def start_timer(self):
        if not self.timer_running:
            self.current_subject = self.subject_box.currentText()
            self.start_time = time.time()
            self.timer_running = True
            self.qtimer.start(1000)

    def stop_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.tracker.log_time(self.current_subject, elapsed)
            self.timer_running = False
            self.qtimer.stop()
            self.update_table()
            self.timer_label.setText("00:00:00")

            if self.history_tab:
                self.history_tab.update_table()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        self.timer_label.setText(f"{h:02}:{m:02}:{s:02}")

    def update_table(self):
        data = self.tracker.get_today()

        subjects = self.tracker.subjects
        self.table.setRowCount(len(subjects) + 1)  # subjects + TOTAL

        total_seconds = 0
        for row, subject in enumerate(subjects):
            time_str = data.get(subject, "00:00:00")
            self.table.setItem(row, 0, QTableWidgetItem(subject))
            self.table.setItem(row, 1, QTableWidgetItem(time_str))

            h, m, s = map(int, time_str.split(":"))
            total_seconds += h * 3600 + m * 60 + s

        #Creates TOTAL row
        total_str = f"{total_seconds//3600:02d}:{(total_seconds%3600)//60:02d}:{total_seconds%60:02d}"
        self.table.setItem(len(subjects), 0, QTableWidgetItem("TOTAL"))
        self.table.setItem(len(subjects), 1, QTableWidgetItem(total_str))