import csv
from dataclasses import dataclass
import requests
from typing import Optional
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/uk/courses"

@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: Optional[int] = None
    topics_count: Optional[int] = None

def parse_single_course(course_block: Tag) -> Course:
    name = course_block.select_one(".ProfessionCard_title__m7uno").get_text(strip=True)
    short_description = course_block.select_one(".ProfessionCard_description__K8weo").get_text(strip=True)
    duration = course_block.select_one(".ProfessionCard_duration__13PwX").get_text(strip=True)

    return Course(name, short_description, duration, None, None)

def get_all_courses() -> list[Course]:
    resp = requests.get(BASE_URL)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__BCg0O")

    courses = [parse_single_course(el) for el in course_elements]
    return courses

def write_courses_to_csv(courses: list[Course]) -> None:
    with open("courses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "short_description", "duration", "modules_count", "topics_count"])
        for course in courses:
            writer.writerow([
                course.name,
                course.short_description,
                course.duration,
                course.modules_count if course.modules_count is not None else "",
                course.topics_count if course.topics_count is not None else ""
            ])

if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)

    write_courses_to_csv(courses)
