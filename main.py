#
#   This script tracks empty quotas in Bilkent classes
#   Designed for class registration
#   Made by Tolga Ozgun
#   https://github.com/tolgaozgun
#

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
# import winsound
# from win32com.client import Dispatch
import json
import os

# speak = Dispatch("SAPI.SpVoice").Speak

courses = {}
frequency = 2500
duration = 1000
delay = 1


os.system('say "Bilkent Quota Tracker loaded."')


def print_with_time(message: str):
    t = datetime.now()
    current_time = t.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3] + " | "
    print(str(current_time) + message)


def section_id_filler(id: str):
    for i in range(len(id), 3):
        id = "0" + id
    return id


def failed_response_handler(response_code: int):
    if response_code == 200:
        return

    if response_code == 429:
        print_with_time(f"Request marked as spam, retrying in a second.")
    else:
        print_with_time(f"Connection error to servers, check your connection! Retrying in {delay} second(s)."
                        f"Error code: [{response_code}]")


def remove_section(course_code: str, section_id: int):
    section_ids = courses[course_code]
    for cur_section_id in section_ids:
        if int(cur_section_id) == int(section_id):
            section_ids.remove(cur_section_id)
    if len(section_ids) == 0:
        print(f"No section left for {course_code} while removing section: {section_id}. Removing course instead")
        courses.pop(course_code)
        return
    courses[course_code] = section_ids


def find_course(course_code: str, section_ids):
    global r
    final_sections = []

    for section_id in section_ids:
        final_sections.append(section_id_filler(section_id))

    URL = f"https://stars.bilkent.edu.tr/homepage/ajax/course.sections.php?COURSE={course_code}&SEMESTER=20231"
    response_code = 0

    while response_code != 200:
        r = requests.get(URL)
        response_code = r.status_code
        if response_code != 200:
            failed_response_handler(response_code)
            time.sleep(delay)

    if r.text.__contains__("no section"):
        print_with_time(f"Course does not exist: {course_code}. Removing this course for now")
        courses.pop(course_code)
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    for section in final_sections:
        table_id = f"{course_code}-{section}"
        table = soup.find('tr', attrs={'id': table_id})
        if table is None:
            print(f"Section does not exist for {table_id}. Removing this section for now")
            remove_section(course_code, section)
            continue
        col = table.findAll('td', attrs={'align': 'center'})[6]
        quota = int(col.text)
        if quota == 0:
            continue
        else:
            print_with_time(f"Course {table_id} has {quota} quota!")
            os.system(f'say "Course {table_id} has {quota} quota!"')
            # speak(f"Course {table_id} has {quota} quota!")


def read_config():
    with open("config.json", "r") as json_file:
        data = json.load(json_file)

        global frequency
        global duration
        global delay

        if data["voice"]["frequency"] and int(data["voice"]["frequency"]) is not None:
            frequency = int(data["voice"]["frequency"])
        else:
            print(f"Error reading voice frequency from config.")
        print(f"Voice frequency set to: {frequency}")

        if data["voice"]["duration"] and int(data["voice"]["duration"]) is not None:
            duration = int(data["voice"]["duration"])
        else:
            print(f"Error reading voice duration from config.")
        print(f"Voice duration set to: {duration}")

        # Convert delay in milliseconds to seconds
        if data["request"]["delay"] and float(data["request"]["delay"]) is not None:
            delay = float(data["request"]["delay"]) / 1000.0
        else:
            print(f"Error reading request delay from config.")
        print(f"Delay is set to: {delay}")

        if not data["courses"] or len(data["courses"]) == 0:
            print_with_time("No courses added to config!")

        for course in data["courses"]:
            sections = data["courses"][course]
            print(f"Loaded {course} with sections:", end=" ")
            count = 1
            for section in sections:
                divider = ", "
                if count == len(sections):
                    divider = ""
                print(f"{section}", end=divider)
                count += 1
            courses[course] = sections
            print()


def main():
    read_config()

    # Start an infinite loop
    while 1:
        try:
            for course in courses.keys():
                print_with_time(f"Looking for {course}")
                section_ids = courses[course]
                find_course(course, section_ids)
                # Wait for one second until the next course.
                time.sleep(delay)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

