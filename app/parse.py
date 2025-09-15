import csv
from dataclasses import dataclass
import requests
from typing import Optional, List
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
    name_tag = course_block.select_one(".ProfessionCard_title__m7uno")
    name = name_tag.get_text(strip=True) if name_tag else ""

    desc_tag = course_block.select_one(".ProfessionCard_description__K8weo")
    short_description = desc_tag.get_text(strip=True) if desc_tag else ""

    dur_tag = course_block.select_one(".ProfessionCard_duration__13PwX")
    duration = dur_tag.get_text(strip=True) if dur_tag else ""

    return Course(name, short_description, duration, None, None)

def get_all_courses() -> List[Course]:
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    if not course_elements:
        print("No courses found on the page")
        return []

    courses = []
    for el in course_elements:
        try:
            course = parse_single_course(el)
            courses.append(course)
        except Exception as e:
            print(f"Error parsing course card: {e}")
            continue

    return courses

def write_courses_to_csv(courses: List[Course]) -> None:
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
    print(f"{len(courses)} courses written to courses.csv")
