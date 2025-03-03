'''
STUDY TRACKER BETA
Author: Eric Wing

'''
import time
from datetime import date
import json
import sys
from pathlib import Path


def convert_to_hms(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def convert_to_s(t):

    hours = 0
    minutes = 0
    seconds = 0

    if int(t[0]) > 0:
        hours += int(t[0]) * 10
    if int(t[1]) > 0:
        hours += int(t[1])

    if int(t[3]) > 0:
        minutes += int(t[3]) * 10
    if int(t[4]) > 0:
        minutes += int(t[4])

    if int(t[6]) > 0:
        seconds += int(t[6]) * 10
    if int(t[7]) > 0:
        seconds += int(t[7]) 

    seconds += hours * 3600
    seconds += minutes * 60
    return seconds


def track(option, courses):

    selection = ""
    subject = courses[int(option) - 1]
    total_subject_time = convert_to_s(daily_log[subject])

    total_time = convert_to_s(daily_log["TOTAL"])
    
    print("Subject", subject, "selected. Starting timer...")

    start = time.time()

    while not selection == "STOP":
        selection = input("Enter [STOP] to end session\n")
    
    end = time.time()

    seconds = int(end - start)
    out = convert_to_hms(seconds)

    total_subject_time += seconds
    total_time += seconds

    daily_log[subject] = convert_to_hms(total_subject_time)
    daily_log["TOTAL"] = convert_to_hms(total_time)

    print("You studied", subject, "for", out)

def create_account(courses, save_file):
    daily_log = dict()
    weekly_log = dict()

    for course in courses:
        daily_log[course] = "00:00:00"

    daily_log["TOTAL"] = "00:00:00"
    weekly_log[str(date.today())] = daily_log

    with open(save_file, 'w') as f:
            json.dump(weekly_log, f)


    

if __name__ == "__main__":

    changes_made = False
    daily_log = dict()
    
    
    print("----------------------------------------------------------------")
    print("--------------WELCOME TO STUDY TRACKER (BETA 1.3)---------------")
    print("----------------------------------------------------------------")

    save_file = Path("log.json")

    if not save_file.exists():
        
        print("Account not found.")

        while True:

            x = input("Would you like to create a new account? [y/n]")

            if (x.lower() == 'y'):
                save_file.touch()
                
                print()
                courses = input("Enter your courses (separate each course name with a space): ").split()
                
                create_account(courses, save_file)
                print()
                print("Account created!")
                print()
                break
            elif (x.lower() == 'n'):
                sys.exit()
            else:
                print("Invalid input.")


    

    with open(save_file, 'r') as f:  
        weekly_log = json.load(f)

    today = str(date.today())
    last_date = list(weekly_log.keys())[-1]

    subjects = list(weekly_log[last_date].keys())[:-1]

#Check for date change
    if last_date == today: 
        daily_log = weekly_log[last_date]
        print("Welcome back!")
    else:
#New date:
        weekly_log[today] = daily_log

        for subject in subjects:
            daily_log[subject] = "00:00:00"

        daily_log["TOTAL"] = "00:00:00"
        changes_made = True
        print("Today is", today)

    while True:

        print()
        selection = input("[1] Track Study Time\n" +
                        "[2] See Today's Progress\n" +
                        "[3] See Log\n" +
                        "[4] Delete Account\n" +
                        "[q] Quit\n")

        match selection:
            case "1":
                print()
                print("Select Subject:")

                for i in range(len(subjects)):
                    print("[", i + 1, "] ", subjects[i], "\n", sep="", end="")

                selection = input()

                print()
                track(selection, subjects)
                print()

                changes_made = True
            
            case "2":
                print()
                print("-" * 16)
                print("Today's Hours:")

                for i in range(len(subjects)):
                    print(subjects[i], "  ", daily_log[subjects[i]])

                print()
                print("Time spent studying today:", daily_log["TOTAL"])
                print("-" * 16)
                print()
                print("Press any key to continue...")
                selection = input()
                print()

            case "3":

                with open(save_file, 'r') as f2:
                    weekly_log = json.load(f2)

                print()
                print("Log:")
                print_dict = dict()

                for key in weekly_log:
                    print_dict = weekly_log[key]
                    print(key, ":", sep="")
                        
                    for i in range(len(subjects)):
                        print(subjects[i], "[", print_dict[subjects[i]], "] ", sep="")
                
                print()
                print("Press any key to continue...")
                selection = input()
                print()
                            
            case "4":
                x = input("Are you sure you want to delete your account? [y/n]")

                if x.lower() == 'y':
                    save_file.unlink()
                    print("Account deleted.")
                    print("Study_Tracker will now restart.\n")
                    sys.exit()

            case "q":
                break

    if changes_made:
        with open(save_file, 'w') as f:
            json.dump(weekly_log, f)
            print("Progress saved.")

    print()
    print("SESSION END")
    sys.exit()
    