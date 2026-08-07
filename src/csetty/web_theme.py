# ruff: noqa: E501
from __future__ import annotations

import html

THEME_NAME = "cse-course-exam-v1"


def course_theme_class(profile: str, course: str = "") -> str:
    """Return the local theme variant matching the public course exam pages."""
    identity = f"{profile} {course}".lower()
    if "1521" in identity:
        return "course-comp1521"
    return "course-comp1511"


def theme_style() -> str:
    """Render the shared, offline COMP1511/COMP1521 exam-page theme."""
    return f'<style data-csetty-theme="{THEME_NAME}">{CSE_COURSE_EXAM_CSS}</style>'


def course_navbar(
    *,
    course: str,
    home_url: str,
    links: str,
    status: str = "",
) -> str:
    """Render the shared course-colour navigation shell."""
    status_html = f'<div class="navbar-status">{status}</div>' if status else ""
    return (
        '<nav class="course-navbar no-print" aria-label="Exam navigation">'
        '<div class="container navbar-inner">'
        f'<a class="navbar-brand" href="{html.escape(home_url, quote=True)}">'
        f"{html.escape(course)} — CSEExamTTY</a>"
        f'<div class="navbar-links">{links}</div>{status_html}'
        "</div></nav>"
        f'<script data-csetty-theme-script="{THEME_NAME}">'
        "(() => {"
        "const nav = document.currentScript.previousElementSibling;"
        "if (!nav) return;"
        "const menus = [...nav.querySelectorAll('.nav-menu')];"
        "for (const menu of menus) {"
        "for (const link of menu.querySelectorAll('a')) {"
        "link.addEventListener('click', () => menu.removeAttribute('open'));"
        "}"
        "}"
        "document.addEventListener('click', event => {"
        "for (const menu of menus) {"
        "if (!menu.contains(event.target)) menu.removeAttribute('open');"
        "}"
        "});"
        "document.addEventListener('keydown', event => {"
        "if (event.key === 'Escape') {"
        "for (const menu of menus) menu.removeAttribute('open');"
        "}"
        "});"
        "})();</script>"
    )


CSE_COURSE_EXAM_CSS = r"""
:root {
  --course-accent: #6abd6e;
  --course-nav: #397d3d;
  --course-soft: #edf8ee;
  --content-width: 64rem;
  --body-color: #212529;
  --muted: #6c757d;
  --border: #dee2e6;
  --light: #f8f9fa;
  --jumbotron: #e9ecef;
  --success: #155724;
  --success-bg: #d4edda;
  --success-border: #c3e6cb;
  --warning: #856404;
  --warning-bg: #fff3cd;
  --warning-border: #ffeeba;
  --danger: #721c24;
  --danger-bg: #f8d7da;
  --danger-border: #f5c6cb;
}
body.course-comp1521 {
  --course-accent: #42a097;
  --course-nav: #28766f;
  --course-soft: #e8f5f4;
  --content-width: 56rem;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 5rem; }
body {
  margin: 0;
  background: #fff;
  color: var(--body-color);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, "Noto Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  text-align: left;
}
a { color: #0056b3; text-decoration: none; }
a:hover { color: #003f83; text-decoration: underline; }
.container {
  width: 100%;
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 0 15px;
}
.course-navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  color: #fff;
  background: var(--course-nav);
  box-shadow: 0 1px 3px rgba(0, 0, 0, .18);
}
.navbar-inner {
  min-height: 3.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.navbar-brand {
  flex: 0 0 auto;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 500;
  white-space: nowrap;
}
.navbar-brand:hover, .course-navbar a:hover { color: #fff; text-decoration: underline; }
.navbar-links {
  display: flex;
  align-items: center;
  gap: .2rem;
  min-width: 0;
}
.navbar-links > a, .nav-menu > summary {
  display: block;
  color: rgba(255, 255, 255, .92);
  padding: .85rem .65rem;
  cursor: pointer;
  white-space: nowrap;
}
.nav-menu { position: relative; }
.nav-menu > summary { list-style: none; }
.nav-menu > summary::-webkit-details-marker { display: none; }
.nav-menu > summary::after { content: " ▾"; }
.nav-menu[open] > summary::after { content: " ▴"; }
.nav-menu-items {
  position: absolute;
  top: calc(100% - .15rem);
  left: 0;
  z-index: 1010;
  width: min(24rem, calc(100vw - 2rem));
  max-height: min(70vh, 34rem);
  overflow: auto;
  padding: .5rem 0;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, .15);
  border-radius: .25rem;
  box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .175);
}
.nav-menu-items a {
  display: block;
  color: #212529;
  padding: .35rem 1.5rem;
  white-space: normal;
}
.nav-menu-items a:hover, .nav-menu-items a[aria-current="page"] {
  color: #16181b;
  background: #f1f3f5;
  text-decoration: none;
}
.navbar-status {
  display: flex;
  align-items: center;
  gap: .55rem;
  margin-left: auto;
  white-space: nowrap;
  font-size: .9rem;
}
main.container { padding-top: 1rem; padding-bottom: 2rem; }
.exam-hero {
  margin: 0 0 2rem;
  padding: 2rem 1rem;
  text-align: center;
  background: var(--jumbotron);
  border-radius: .3rem;
}
.exam-hero h1 {
  margin: 0 0 .5rem;
  font-size: clamp(2rem, 6vw, 3.5rem);
  font-weight: 300;
  line-height: 1.2;
}
.exam-hero p { margin: .25rem 0; }
.lead { font-size: 1.2rem; font-weight: 300; }
.text-muted, .muted { color: var(--muted); }
.text-uppercase { text-transform: uppercase; letter-spacing: .035em; }
.exam-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}
.section-heading {
  margin-bottom: 1rem;
  padding: .75rem 1.25rem;
  border: 1px solid var(--course-accent);
  border-left-width: .5rem;
  border-radius: .25rem;
  background: #fff;
}
.section-heading h2, .section-heading h3 { margin: 0; color: #212529; }
.section-heading p { margin: .25rem 0 0; color: var(--muted); }
.card {
  position: relative;
  min-width: 0;
  margin-bottom: 1rem;
  overflow-wrap: anywhere;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, .125);
  border-radius: .25rem;
}
.card-body { padding: 1.25rem; }
.card h2:first-child, .card h3:first-child { margin-top: 0; }
.alert {
  position: relative;
  margin: 0 0 1rem;
  padding: .75rem 1.25rem;
  border: 1px solid transparent;
  border-radius: .25rem;
}
.alert h2, .alert h3 { margin-top: 0; }
.alert-success { color: var(--success); background: var(--success-bg); border-color: var(--success-border); }
.alert-warning { color: var(--warning); background: var(--warning-bg); border-color: var(--warning-border); }
.alert-danger { color: var(--danger); background: var(--danger-bg); border-color: var(--danger-border); }
.alert-course { color: #243c28; background: var(--course-soft); border-color: var(--course-accent); }
.btn {
  display: inline-block;
  padding: .5rem .75rem;
  color: #fff;
  font: inherit;
  font-weight: 600;
  line-height: 1.25;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  background: var(--course-nav);
  border: 1px solid var(--course-nav);
  border-radius: .25rem;
}
.btn:hover { color: #fff; filter: brightness(.9); text-decoration: none; }
.actions { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1rem 0 0; }
.badge {
  display: inline-block;
  margin: .1rem .2rem .1rem 0;
  padding: .25em .5em;
  color: #fff;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  vertical-align: baseline;
  background: #6c757d;
  border-radius: .25rem;
}
table { width: 100%; margin-bottom: 1rem; border-collapse: collapse; }
th, td { padding: .55rem; text-align: left; vertical-align: top; border: 1px solid var(--border); }
thead th { vertical-align: bottom; background: var(--light); }
.table-scroll { width: 100%; overflow-x: auto; }
dl { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: .25rem 1rem; }
dt { font-weight: 700; }
dd { margin: 0; overflow-wrap: anywhere; }
code, kbd, pre, samp { font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
code {
  padding: .2em .4em;
  color: inherit;
  font-size: 85%;
  white-space: break-spaces;
  background: rgba(27, 31, 35, .06);
  border-radius: 3px;
}
pre {
  max-width: 100%;
  overflow: auto;
  margin: .5rem 0 1rem;
  padding: .5rem;
  color: #212529;
  white-space: pre;
  background: #f8f8f8;
  border: 1px solid #eee;
  border-radius: .25rem;
  tab-size: 4;
}
pre code { padding: 0; white-space: pre; background: transparent; }
blockquote {
  margin: 1rem 0;
  padding: .5rem 1rem;
  color: #555;
  background: #f9f9f9;
  border-left: .5rem solid #ccc;
}
details.report-detail { border-top: 1px solid var(--border); padding: .8rem 0; }
details.report-detail > summary { cursor: pointer; font-weight: 700; }
.resource-grid { columns: 2 18rem; column-gap: 2rem; }
.resource-section { break-inside: avoid; margin-bottom: 1rem; }
.resource-section h3 { margin-bottom: .25rem; }
.resource-section ul { margin-top: .25rem; }
@media (max-width: 760px) {
  .navbar-inner { align-items: flex-start; flex-wrap: wrap; gap: 0 .5rem; padding-top: .35rem; padding-bottom: .35rem; }
  .navbar-brand { width: 100%; }
  .navbar-links { order: 2; }
  .navbar-status { align-self: center; margin-left: auto; }
  .navbar-links > a, .nav-menu > summary { padding: .45rem .5rem; }
  .nav-menu-items { position: fixed; top: 6.8rem; left: 1rem; }
  .exam-hero { padding: 1.5rem .8rem; }
  .lead { font-size: 1.05rem; }
  .card-body, .section-heading { padding: .85rem; }
  dl { grid-template-columns: 1fr; gap: .1rem; }
  dd { margin-bottom: .5rem; }
  .resource-grid { columns: 1; }
}
@media print {
  .no-print { display: none !important; }
  .exam-hero { break-after: avoid; }
  .exam-section, .card { break-inside: avoid; }
}
"""
