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
import winsound
from win32com.client import Dispatch

speak = Dispatch("SAPI.SpVoice").Speak


def print_with_time(message: str):
    t = datetime.now()
    current_time = t.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3] + " | "
    print(str(current_time) + message)


def section_id_filler(id: str):
    for i in range(len(id), 3):
        id = "0" + id
    return id


def find_course(course_code: str, section_ids):
    final_sections = []

    for section_id in section_ids:
        final_sections.append(section_id_filler(section_id))

    URL = f"https://stars.bilkent.edu.tr/homepage/ajax/course.sections.php?COURSE={course_code}&SEMESTER=20221"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    for section in final_sections:
        table_id = f"{course_code}-{section}"
        table = soup.find('tr', attrs={'id': table_id})
        col = table.findAll('td', attrs={'align': 'center'})[6]
        result = col.encode_contents()
        result = str(result)
        empty_result = 'b\'0\''
        if result == empty_result:
            continue
        else:
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            print_with_time(f"Course {table_id} has slot! -> {result}")
            speak(f"Lesson {table_id} is available")


def main():
    # Start an infinite loop
    while 1:
        try:
            print_with_time("Script is still running..")
            course = "THR 110"
            section_ids = ["2"]
            find_course(course, section_ids)

            course = "MATH 225"
            section_ids = ["3", "5"]
            find_course(course, section_ids)

            course = "HUM 111"
            section_ids = ["35"]
            find_course(course, section_ids)

            # Wait for one second until the next request.
            time.sleep(1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

