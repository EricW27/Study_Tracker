'''
STUDY TRACKER BETA
Author: Eric Wing

Backend Logic

'''

import os, json
from datetime import date
from pathlib import Path

class StudyTracker:
    def __init__(self, save_path="log.json"):
        self.save_file = Path(save_path)
        self.weekly_log = {}
        self.daily_log = {}
        self.subjects = []
        self.today = str(date.today())
        self.load_or_create()

    #Locates JSON save data
    def load_or_create(self):

        if not self.save_file.exists():
            return

        with open(self.save_file, 'r') as f:
            self.weekly_log = json.load(f)

        #Strip TOTAL from all logs (legacy cleanup)
        for log in self.weekly_log.values():
            log.pop("TOTAL", None)

        try:
            last_date = max(self.weekly_log.keys(), key=lambda d: date.fromisoformat(d))
        except Exception:
            #fallback: previous behavior
            last_date = list(self.weekly_log.keys())[-1]

        self.subjects = list(self.weekly_log[last_date].keys())

        #Use today's log or initialize a new one
        if last_date == self.today:
            self.daily_log = self.weekly_log[last_date]
        else:
            self.daily_log = {sub: "00:00:00" for sub in self.subjects}
            self.weekly_log[self.today] = self.daily_log

        
    #Creates account with given list of courses
    def create_account(self, courses):
        self.subjects = courses
        self.daily_log = {c: "00:00:00" for c in courses}
        self.weekly_log[self.today] = self.daily_log
        self.save()

    #Save data
    def save(self):
        self.weekly_log[self.today] = self.daily_log
        with open(self.save_file, 'w') as f:
            json.dump(self.weekly_log, f)

    def _is_reserved(self, name: str) -> bool:
        return name.strip().upper() == "TOTAL"

    def add_subject(self, subject_name: str):
        subject_name = subject_name.strip()
        if not subject_name or self._is_reserved(subject_name):
            return
        if any(s.lower() == subject_name.lower() for s in self.subjects):
            return
        
        self.subjects.append(subject_name)
        self.daily_log[subject_name] = "00:00:00"

        for log in self.weekly_log.values():
            log.setdefault(subject_name, "00:00:00")

        self.save()

    def rename_subject(self, old_name: str, new_name: str):
        new_name = new_name.strip()
        if (old_name not in self.subjects or
            not new_name or
            self._is_reserved(old_name) or
            self._is_reserved(new_name) or
            any(s.lower() == new_name.lower() for s in self.subjects)):
            return

        idx = self.subjects.index(old_name)
        self.subjects[idx] = new_name

        for log in self.weekly_log.values():
            if old_name in log:
                log[new_name] = log.pop(old_name)

        self.save()

    def delete_subject(self, subject_name: str):
        if subject_name not in self.subjects:
            return
        
        #Remove from subjects list
        self.subjects.remove(subject_name)

        #Remove from logs
        for log in self.weekly_log.values():
            if subject_name in log:
                del log[subject_name]

        self.save()


    def get_today(self):
        return self.daily_log
    
    def log_time(self, subject, seconds):
        #Helper functions for calculations
        def to_s(hms):
            h, m, s = map(int, hms.split(":"))
            return h*3600 + m*60 + s
        def to_hms(secs):
            h, secs = divmod(secs, 3600)
            m, secs = divmod(secs, 60)
            return f"{h:02}:{m:02}:{secs:02}"
        
        if subject not in self.daily_log:
            return
        
        self.daily_log[subject] = to_hms(to_s(self.daily_log[subject]) + seconds)
        self.save()