'''
STUDY TRACKER BETA
Author: Eric Wing

History Tab

'''
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem)

class HistoryTab(QWidget):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_table()

    def update_table(self):
        
        subjects = self.tracker.subjects

        #Sort by date descending (newest first)
        sorted_items = sorted(
            self.tracker.weekly_log.items(),
            key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"),
            reverse=True
        )

        #Reset table 
        self.table.clear()
        self.table.setRowCount(len(sorted_items))
        self.table.setColumnCount(len(subjects) + 2)
        self.table.setHorizontalHeaderLabels(["Date"] + subjects + ["TOTAL"])

        #Fill table
        for row_idx, (day, log) in enumerate(sorted_items):
            self.table.setItem(row_idx, 0, QTableWidgetItem(day))

            total_seconds = 0

            for col_idx, sub in enumerate(subjects, start=1):

                time_str = log.get(sub, "00:00:00")
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(time_str))

                #Convert hh:mm:ss string to seconds for summing
                h, m, s = map(int, time_str.split(":"))
                total_seconds += h * 3600 + m * 60 + s
            
            total_str = f"{total_seconds//3600:02d}:{(total_seconds%3600)//60:02d}:{total_seconds%60:02d}"
            self.table.setItem(row_idx, len(subjects) + 1, QTableWidgetItem(total_str))