# ruff: noqa: E501
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CourseResourceLink:
    section: str
    label: str
    url: str


def _comp1511_links() -> tuple[CourseResourceLink, ...]:
    base = "https://cgi.cse.unsw.edu.au/~cs1511/26T2"
    links = [
        CourseResourceLink("Course", "Course home and complete index", f"{base}/"),
        CourseResourceLink("Course", "Course outline", f"{base}/outline"),
        CourseResourceLink("Guides", "C style guide", f"{base}/resources/style_guide.html"),
        CourseResourceLink("Guides", "C reference sheet", f"{base}/resources/c-reference-sheet.pdf"),
        CourseResourceLink("Guides", "COMP1511 cheat sheet", f"{base}/resources/1511_cheatsheet.html"),
        CourseResourceLink("Guides", "Debugging guide", f"{base}/resources/debugging_guide.html"),
        CourseResourceLink("Guides", "Home computing setup", f"{base}/resources/home_computing.html"),
        CourseResourceLink("Guides", "Learning flowchart", f"{base}/resources/flowchart.html"),
        CourseResourceLink("Guides", "VS Code Live Share setup", f"{base}/resources/vscode_liveshare_setup.html"),
        CourseResourceLink("Guides", "Terminal accessibility", f"{base}/resources/accessibility.html"),
        CourseResourceLink("Lectures", "Lecture slide index", f"{base}/slides/"),
        CourseResourceLink("Exam preparation", "Revision videos", f"{base}/resources/revision_videos.html"),
        CourseResourceLink("Exam preparation", "Practice exam solutions", f"{base}/resources/prac-exam-solns.html"),
        CourseResourceLink("Assignments", "Assignment 1", f"{base}/assignments/ass1/index.html"),
        CourseResourceLink("Assignments", "Assignment 2", f"{base}/assignments/ass2/index.html"),
        CourseResourceLink("Supplementary", "SplashKit activity", f"{base}/activity/splashkit_master"),
    ]
    lecture_recordings = {
        1: (
            ("A", "https://youtube.com/live/TZWsHuGO-qU?feature=share"),
            ("B", "https://youtube.com/live/DE6XQud6tRs?feature=share"),
        ),
        2: (
            ("A", "https://youtu.be/pIIENaImoH0"),
            ("B", "https://youtube.com/live/B3BG-BP6gw0?feature=share"),
        ),
        3: (
            ("A", "https://youtube.com/live/9wHQQIbqgNA?feature=share"),
            ("B", "https://youtube.com/live/nwjsgwAbtK4?feature=share"),
        ),
        4: (
            ("A", "https://youtube.com/live/B3rYDcrVfYk?feature=share"),
            ("B", "https://youtube.com/live/e_HWFJATWvU?feature=share"),
        ),
        5: (
            ("A", "https://youtube.com/live/8VtFEFmFj04?feature=share"),
            ("B", "https://youtube.com/live/3rb8Sfurl3Y?feature=share"),
        ),
        7: (
            ("A", "https://youtube.com/live/6rbnc_LmAwM?feature=share"),
            ("B", "https://youtube.com/live/vIIK76zr2Wg?feature=share"),
        ),
        8: (
            ("A", "https://youtube.com/live/CAo1MyIX_70?feature=share"),
            ("B", "https://youtube.com/live/ZkJXOopVemc?feature=share"),
        ),
        9: (
            ("A", "https://youtube.com/live/_ll5fWsoLJY?feature=share"),
            ("B", "https://youtube.com/live/kKQWX_eGrgE?feature=share"),
        ),
        10: (
            ("A", "https://youtube.com/live/4BUd91qb6dM?feature=share"),
            ("B", "https://youtube.com/live/B5GVNJtM93A?feature=share"),
        ),
    }
    teaching_weeks = (1, 2, 3, 4, 5, 7, 8, 9, 10)
    for week in teaching_weeks:
        number = f"{week:02d}"
        links.extend(
            (
                CourseResourceLink(
                    "Lecture materials", f"Week {number} lecture slides", f"{base}/slides/week_{week}/"
                ),
                CourseResourceLink(
                    "Lecture materials", f"Week {number} lecture code", f"{base}/code/week_{week}/"
                ),
                CourseResourceLink(
                    "Tutorials", f"Week {number} tutorial activities", f"{base}/tut/{number}/questions"
                ),
                CourseResourceLink(
                    "Problem sets", f"Week {number} problem set", f"{base}/lab/{number}/questions"
                ),
            )
        )
        links.extend(
            CourseResourceLink(
                "Lecture recordings",
                f"Week {number} lecture recording {slot}",
                url,
            )
            for slot, url in lecture_recordings[week]
        )
    for week in (1, 2, 3, 4, 5, 7):
        number = f"{week:02d}"
        links.append(
            CourseResourceLink(
                "Sample solutions",
                f"Week {number} laboratory sample solutions",
                f"{base}/lab/{number}/answers",
            )
        )
    for week in (2, 3, 4, 5, 7, 8, 9, 10):
        number = f"{week:02d}"
        links.append(
            CourseResourceLink(
                "Extra challenges",
                f"Week {number} challenge exercises",
                f"{base}/challenges/{number}/questions",
            )
        )
    for week in (4, 5, 6, 7, 8, 10):
        number = f"{week:02d}"
        links.append(
            CourseResourceLink(
                "Extra revision",
                f"Week {number} revision questions",
                f"{base}/revision/{number}/questions",
            )
        )
        if week != 10:
            links.append(
                CourseResourceLink(
                    "Extra revision",
                    f"Week {number} revision sample solutions",
                    f"{base}/revision/{number}/answers",
                )
            )
    return tuple(links)


def _comp1521_links() -> tuple[CourseResourceLink, ...]:
    base = "https://cgi.cse.unsw.edu.au/~cs1521/26T1"
    links = [
        CourseResourceLink("Course", "Course home and complete index", f"{base}/"),
        CourseResourceLink("Course", "Course outline", f"{base}/outline/"),
        CourseResourceLink("Course", "Course handbook entry", f"{base}/handbook/ug/"),
        CourseResourceLink("Guides", "C style guide", f"{base}/resources/c_style_guide.html"),
        CourseResourceLink("Guides", "Assembly style guide", "https://jashankj.space/notes/cse-comp1521-better-assembly/"),
        CourseResourceLink("Guides", "MIPS instruction set", f"{base}/resources/mips-guide.html"),
        CourseResourceLink("Guides", "MIPS editor setup", f"{base}/resources/mips-editors.html"),
        CourseResourceLink("Guides", "Linux cheat sheet", f"{base}/resources/linux-cheatsheet.html"),
        CourseResourceLink("Guides", "C quick reference", f"{base}/resources/cheatsheets/c-qrc.pdf"),
        CourseResourceLink("MIPS tools", "mipsy web", "https://cgi.cse.unsw.edu.au/~cs1521/mipsy/"),
        CourseResourceLink("MIPS tools", "mipsy source repository", "https://github.com/insou22/mipsy"),
        CourseResourceLink("Exam preparation", "Released practice exams", f"{base}/resources/practice_exams.html"),
        CourseResourceLink("Lecture materials", "Lecture slide index", f"{base}/slides/"),
        CourseResourceLink("Lecture materials", "Live lecture code index", f"{base}/live/"),
        CourseResourceLink("Lecture materials", "Lecture streams and recordings", f"{base}/lectures/"),
        CourseResourceLink("Assignments", "Assignment 1", f"{base}/assignments/ass1/index.html"),
        CourseResourceLink("Assignments", "Assignment 2", f"{base}/assignments/ass2/index.html"),
        CourseResourceLink(
            "Topic supplements",
            "Floating-point lecture video",
            "https://youtu.be/KNbPIi-qpEI",
        ),
        CourseResourceLink(
            "Topic supplements",
            "IEEE 754 single-precision reference",
            "https://en.wikipedia.org/wiki/Single-precision_floating-point_format",
        ),
        CourseResourceLink(
            "Topic supplements",
            "Floating-point calculator",
            "https://www.h-schmidt.net/FloatConverter/IEEE754.html",
        ),
    ]
    topics = (
        ("MIPS basics", "mips_basics"),
        ("MIPS control", "mips_control"),
        ("MIPS data", "mips_data"),
        ("MIPS functions", "mips_functions"),
        ("Integer representation", "integers"),
        ("Bitwise operations", "bitwise_operations"),
        ("Floating point", "floating_point"),
        ("Files", "files"),
        ("Unicode", "unicode"),
        ("Processes", "processes"),
        ("Threads", "threads"),
    )
    for label, slug in topics:
        links.extend(
            (
                CourseResourceLink("Topic notes", f"{label} notes", f"{base}/topic/{slug}/notes"),
                CourseResourceLink("Topic code", f"{label} code", f"{base}/topic/{slug}/code/"),
            )
        )
    for week in (1, 2, 3, 4, 5, 7, 8, 9, 10):
        number = f"{week:02d}"
        links.extend(
            (
                CourseResourceLink(
                    "Lecture materials",
                    f"Week {number} lecture slides",
                    f"{base}/slides/week_{number}/",
                ),
                CourseResourceLink(
                    "Tutorials", f"Week {number} tutorial", f"{base}/tut/{number}/questions"
                ),
                CourseResourceLink(
                    "Tutorial answers", f"Week {number} tutorial answers", f"{base}/tut/{number}/answers"
                ),
                CourseResourceLink(
                    "Laboratories", f"Week {number} laboratory", f"{base}/lab/{number}/questions"
                ),
                CourseResourceLink(
                    "Laboratory solutions", f"Week {number} laboratory sample solutions", f"{base}/lab/{number}/answers"
                ),
            )
        )
    for week in (3, 4, 5, 6, 7, 8, 9, 10):
        number = f"{week:02d}"
        links.append(
            CourseResourceLink(
                "Weekly tests", f"Week {number} weekly test", f"{base}/test/{number}/questions"
            )
        )
        links.append(
            CourseResourceLink(
                "Weekly-test answers",
                f"Week {number} weekly-test sample answers",
                f"{base}/test/{number}/answers",
            )
        )
    for label in ("01", "06", "11a", "11b"):
        links.extend(
            (
                CourseResourceLink(
                    "Extra revision", f"Revision {label} questions", f"{base}/revision/{label}/questions"
                ),
                CourseResourceLink(
                    "Extra revision", f"Revision {label} sample solutions", f"{base}/revision/{label}/answers"
                ),
            )
        )
    return tuple(links)


_RESOURCE_LINKS = {
    "comp1511": _comp1511_links(),
    "comp1521": _comp1521_links(),
}


def course_resource_links(profile: str) -> tuple[CourseResourceLink, ...]:
    return _RESOURCE_LINKS.get(profile, ())
