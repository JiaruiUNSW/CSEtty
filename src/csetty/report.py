# ruff: noqa: E501
from __future__ import annotations

import hashlib
import html
import json
import webbrowser
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .grading import render_grade_text
from .models import Attempt
from .pack import Pack, Question
from .util import atomic_write, safe_relative_path
from .web_render import markdown_to_html
from .web_theme import course_navbar, course_theme_class, theme_style

_MAX_EMBEDDED_SOURCE_BYTES = 256 * 1024


def open_report_in_browser(
    html_path: Path,
    *,
    browser_open: Callable[[str], object] = webbrowser.open,
) -> bool:
    """Open a completed local report without making browser failure fatal."""
    if not html_path.is_file():
        return False
    try:
        return bool(browser_open(html_path.resolve().as_uri()))
    except (OSError, webbrowser.Error):
        return False


def _source_document(data: bytes) -> dict[str, Any]:
    clipped = data[:_MAX_EMBEDDED_SOURCE_BYTES]
    return {
        "content": clipped.decode("utf-8", errors="replace"),
        "truncated": len(data) > len(clipped),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def _enrich_submissions(
    submissions: Sequence[Mapping[str, Any]],
    object_reader: Callable[[str], bytes] | None,
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for submission in submissions:
        item = dict(submission)
        files: list[dict[str, Any]] = []
        for file_value in submission.get("files", []):
            file_item = dict(file_value)
            if object_reader is not None:
                source = _source_document(object_reader(str(file_item["object_digest"])))
                file_item.update(source)
            files.append(file_item)
        item["files"] = files
        enriched.append(item)
    return enriched


def _read_authored_text(path: Path) -> dict[str, Any] | None:
    if not path.is_file() or path.is_symlink():
        return None
    return _source_document(path.read_bytes())


def _solution_document(
    *, author_root: Path, question: Question, reveal: bool
) -> dict[str, Any] | None:
    if not reveal:
        return None
    solutions = author_root / "solutions"
    explanation = _read_authored_text(solutions / "explanations" / f"{question.id}.md")
    references: list[dict[str, Any]] = []
    for relative in question.submission_files:
        safe = safe_relative_path(relative, label="reference solution path")
        source = _read_authored_text(solutions / "reference" / Path(*safe.parts))
        if source is not None:
            references.append({"path": relative, **source})
    if explanation is None and not references:
        return None
    return {"explanation": explanation, "reference_files": references}


def _question_documents(
    *,
    attempt: Attempt,
    pack: Pack,
    submissions: Sequence[Mapping[str, Any]],
    grade: Mapping[str, Any] | None,
    author_root: Path,
) -> list[dict[str, Any]]:
    latest: dict[str, Mapping[str, Any]] = {}
    history: dict[str, list[Mapping[str, Any]]] = {}
    for submission in submissions:
        question_id = str(submission["question_id"])
        history.setdefault(question_id, []).append(submission)
        latest[question_id] = submission
    evaluations = (
        {}
        if grade is None
        else {str(item["id"]): item for item in grade.get("questions", [])}
    )
    reveal = attempt.state.terminal
    documents: list[dict[str, Any]] = []
    for index, question in enumerate(pack.questions, start=1):
        documents.append(
            {
                "number": index,
                "id": question.id,
                "title": question.title,
                "kind": question.kind,
                "points": int(question.points) if question.points == int(question.points) else float(question.points),
                "pass_points": int(question.pass_points) if question.pass_points == int(question.pass_points) else float(question.pass_points),
                "difficulty": question.difficulty,
                "track": question.track,
                "tags": list(question.tags),
                "estimated_minutes": question.estimated_minutes,
                "submission_files": list(question.submission_files),
                "prompt_markdown": pack.question_prompt(question),
                "submission": latest.get(question.id),
                "submission_history": history.get(question.id, []),
                "evaluation": evaluations.get(question.id),
                "solution": _solution_document(
                    author_root=author_root,
                    question=question,
                    reveal=reveal,
                ),
            }
        )
    return documents


_ADVICE_BY_TAG = {
    "io": "Rehearse exact prompt-free input/output contracts and check every scan or read result.",
    "input-output": "Rehearse exact prompt-free input/output contracts and check every scan or read result.",
    "conditionals": "Turn the specification into mutually exclusive cases and test every boundary value.",
    "loops": "Write a loop invariant, then test zero, one, final-iteration, and termination behaviour.",
    "enums": "Use named enum values consistently and verify assumptions about their integer ordering.",
    "structs": "Trace which struct instance each field access updates and initialise every field before use.",
    "functions": "Check each function's preconditions, return value, side effects, and parameter types independently.",
    "arrays-1d": "Rehearse empty, single-element, boundary-index, and full-capacity array cases.",
    "arrays-2d": "Write down row/column bounds first and test edges separately from interior cells.",
    "linked-lists": "Trace head, empty, one-node, insertion/deletion, and ownership/freeing cases on paper.",
    "dynamic-memory": "Pair every allocation with a clear owner, failure check, and matching free path.",
    "strings": "Test the empty string, terminator placement, maximum length, and repeated characters.",
    "char-streams": "Distinguish EOF from every valid byte and test the final unterminated input segment.",
    "debugging": "Reproduce the first failing test locally and compare the earliest differing output byte.",
    "pointers": "Draw each pointer target and ownership relationship before changing indirection or allocation code.",
    "recursion": "State the base case and prove that every recursive call moves strictly toward it.",
    "whole-program": "Split parsing, state updates, and output into small testable functions before integrating them.",
    "testing": "Add boundary and adversarial cases before changing code, then retest the smallest failing case.",
    "integer-arithmetic": "Check signed range, operation order, division rules, and zero or negative boundaries.",
    "integer-representation": "Write the fixed-width bit pattern and signedness before applying shifts or masks.",
    "frequency-counting": "Initialise every counter and define the required tie-breaking rule before scanning data.",
    "command-processing": "Separate command parsing from state mutation and test EOF and termination commands.",
    "mips-basics": "Practise mapping each C variable to a register and checking syscall conventions.",
    "mips-control": "Translate one control-flow block at a time and annotate every branch destination.",
    "mips-data": "Annotate element width, alignment, base address, and byte offset for every load or store.",
    "mips-functions": "Audit argument, return, saved-register, stack-frame, and $ra handling on every path.",
    "bitwise": "Use unsigned fixed-width values and derive masks before combining shifts and operators.",
    "floating-point": "Separate sign, exponent, and fraction fields before interpreting special values.",
    "file-io": "Check every open/read/write result and close every descriptor on success and error paths.",
    "binary-data": "Specify byte order, field width, and short-read/write behaviour before decoding binary data.",
    "file-metadata": "Distinguish path metadata from file contents and handle failed stat calls explicitly.",
    "directories": "Make traversal order deterministic and skip dot entries without assuming readdir order.",
    "recursive-traversal": "State the recursion invariant and verify base, inaccessible, and nested-directory cases.",
    "unicode": "Reason in bytes first: validate lead bytes, continuation bytes, truncation, and scalar limits.",
    "utf-8": "Reason in bytes first: validate lead bytes, continuation bytes, truncation, and scalar limits.",
    "processes": "Draw the process tree, close unused resources, and wait for every child you create.",
    "wait-status": "Check normal termination before decoding a child status and wait for the intended PID.",
    "pipes": "Close unused pipe ends immediately so readers receive EOF and writers cannot deadlock.",
    "threads": "Define ownership of shared data, join every thread, and protect each shared mutation.",
    "pthread": "Check every pthread return code and join all successfully created workers before reading results.",
    "partitioning": "Prove that worker ranges are disjoint, complete, and valid for the smallest input.",
    "synchronisation": "Identify the invariant protected by each mutex and keep critical sections small.",
    "make": "Verify dependency edges and recipes with both a clean build and an incremental rebuild.",
    "c-revision": "Reduce the task to small C expressions and confirm types, precedence, and boundary behaviour.",
    "boundary-cases": "List empty, minimum, maximum, final-element, and failure cases before coding.",
    "signed-integers": "Use signed comparisons deliberately and include all-negative and extreme-value tests.",
}


def _feedback(questions: Sequence[Mapping[str, Any]], grade: Mapping[str, Any] | None) -> dict[str, Any]:
    strengths: list[str] = []
    needs_work: list[str] = []
    weak_tags: list[str] = []
    for question in questions:
        evaluation = question.get("evaluation")
        title = f"Q{question['number']} {question['title']}"
        if question.get("submission") is None:
            needs_work.append(f"{title}: no accepted submission was available for final grading.")
            weak_tags.extend(str(tag) for tag in question.get("tags", []))
            continue
        if evaluation is None:
            needs_work.append(f"{title}: the accepted submission has no final evaluation record.")
            weak_tags.extend(str(tag) for tag in question.get("tags", []))
            continue
        if evaluation.get("passed"):
            earned = evaluation.get("points_earned", 0)
            available = evaluation.get("automatic_points", 0)
            strengths.append(f"{title}: passed ({earned}/{available} automatic points).")
            continue
        failed_tests = [
            test
            for group in evaluation.get("groups", [])
            for test in group.get("tests", [])
            if test.get("result") != "PASS"
        ]
        categories = sorted({str(test.get("result", "NOT_PASSED")) for test in failed_tests})
        suffix = ", ".join(categories) if categories else "not enough passing groups"
        needs_work.append(f"{title}: needs more work ({suffix}).")
        weak_tags.extend(str(tag) for tag in question.get("tags", []))

    recommendations: list[str] = []
    for tag in weak_tags:
        advice = _ADVICE_BY_TAG.get(tag)
        if advice and advice not in recommendations:
            recommendations.append(advice)
    if grade is not None:
        for hurdle in grade.get("hurdles", []):
            if not hurdle.get("passed"):
                recommendations.insert(
                    0,
                    f"Prioritise the {hurdle['label']} before another full paper; it is currently not met.",
                )
    if not recommendations and strengths:
        recommendations.append(
            "Repeat the paper under time pressure and explain each solution aloud to check durable understanding."
        )
    if not recommendations:
        recommendations.append(
            "Start with one normal-track question at a time, use public tests, submit, then review the worked solution."
        )
    return {
        "strengths": strengths,
        "needs_work": needs_work,
        "recommendations": recommendations[:8],
    }


def report_document(
    *,
    attempt: Attempt,
    pack: Pack,
    submissions: list[dict[str, Any]],
    grade: Mapping[str, Any] | None,
    object_reader: Callable[[str], bytes] | None = None,
    author_root: Path | None = None,
) -> dict[str, Any]:
    enriched = _enrich_submissions(submissions, object_reader)
    authored = author_root or Path(attempt.pack_path).parent / "author"
    questions = _question_documents(
        attempt=attempt,
        pack=pack,
        submissions=enriched,
        grade=grade,
        author_root=authored,
    )
    return {
        "schema_version": 2,
        "notice": "CSEExamTTY local simulation; no submission was sent to UNSW.",
        "attempt": {
            "id": attempt.id,
            "pack": f"{pack.id}@{pack.version}",
            "pack_digest": pack.digest,
            "course": pack.course,
            "candidate_id": attempt.candidate_id,
            "profile": pack.profile,
            "mode": attempt.mode.value,
            "state": attempt.state.value,
            "created_at": attempt.created_at.isoformat(),
            "deadline_at": None if attempt.deadline_at is None else attempt.deadline_at.isoformat(),
            "finished_at": None if attempt.finished_at is None else attempt.finished_at.isoformat(),
            "finish_reason": attempt.finish_reason,
            "workspace_kind": attempt.workspace_kind.value,
            "image": attempt.image,
            "timed": attempt.timed,
            "network": "on" if attempt.network == "bridge" else attempt.network,
            "editor": attempt.editor,
            "toolchain": dict(attempt.provenance),
        },
        "submissions": enriched,
        "questions": questions,
        "grade": grade,
        "feedback": _feedback(questions, grade),
    }


def render_report_text(document: Mapping[str, Any]) -> str:
    attempt = document["attempt"]
    toolchain = attempt.get("toolchain", {})
    image_metadata = toolchain.get("image", {})
    lines = [
        str(document["notice"]),
        f"Attempt: {attempt['id']}",
        f"Pack: {attempt['pack']}",
        f"Candidate: {attempt.get('candidate_id') or 'practice user'}",
        f"State: {attempt['state']}",
        f"Mode: {attempt['mode']}",
        f"Image: {attempt['image']}",
        f"Image ID: {image_metadata.get('id', 'not recorded')}",
        "",
        "Toolchain:",
    ]
    tools = toolchain.get("tools", {})
    if tools:
        for name, metadata in sorted(tools.items()):
            lines.append(f"  {name}: {metadata.get('version', 'unknown')}")
    else:
        lines.append("  not recorded")
    lines.extend(("", "Accepted submissions:"))
    submissions = document["submissions"]
    if not submissions:
        lines.append("  none")
    else:
        for submission in submissions:
            lines.append(
                f"  {submission['question_id']} #{submission['sequence']} "
                f"{submission['manifest_digest']}"
            )
    grade = document.get("grade")
    if grade:
        lines.extend(("", render_grade_text(grade)))
    else:
        lines.extend(("", "Local automatic grade: not available"))
    feedback = document.get("feedback", {})
    lines.extend(("", "Strengths:"))
    lines.extend(f"  {item}" for item in feedback.get("strengths", []))
    if not feedback.get("strengths"):
        lines.append("  none identified yet")
    lines.extend(("", "Needs work:"))
    lines.extend(f"  {item}" for item in feedback.get("needs_work", []))
    if not feedback.get("needs_work"):
        lines.append("  none identified by automatic tests")
    lines.extend(("", "Final recommendations:"))
    lines.extend(f"  {item}" for item in feedback.get("recommendations", []))
    return "\n".join(lines)


def _code_block(value: object, *, empty: str = "<empty>") -> str:
    text = "" if value is None else str(value)
    return f"<pre><code>{html.escape(text) if text else html.escape(empty)}</code></pre>"


def _test_details(evaluation: Mapping[str, Any] | None) -> str:
    if evaluation is None:
        return "<p>No accepted submission was available for final grading.</p>"
    sections: list[str] = []
    for group in evaluation.get("groups", []):
        tests = []
        for test in group.get("tests", []):
            result = html.escape(str(test.get("result", "UNKNOWN")))
            detail = html.escape(str(test.get("detail", "")))
            comparison = ""
            if test.get("result") != "PASS":
                comparison = (
                    '<details class="report-detail"><summary>Input, expected output, and actual output</summary>'
                    f"<h5>Input</h5>{_code_block(test.get('stdin'))}"
                    f"<h5>Expected stdout</h5>{_code_block(test.get('expected_stdout'))}"
                    f"<h5>Actual stdout</h5>{_code_block(test.get('stdout_preview'))}"
                    f"<h5>Expected stderr</h5>{_code_block(test.get('expected_stderr'))}"
                    f"<h5>Actual stderr</h5>{_code_block(test.get('stderr_preview'))}"
                    f"<h5>Expected exit status</h5>{_code_block(test.get('expected_exit'))}"
                    f"<h5>Actual exit status</h5>{_code_block(test.get('exit_code'))}"
                    "</details>"
                )
            tests.append(
                "<tr>"
                f"<td><code>{html.escape(str(test.get('id', '')))}</code></td>"
                f"<td class=\"result-{result.lower()}\">{result}</td>"
                f"<td>{test.get('duration_ms', 0)} ms</td><td>{detail}{comparison}</td>"
                "</tr>"
            )
        state = "PASS" if group.get("passed") else "FAIL"
        sections.append(
            f"<h4>{html.escape(str(group.get('id')))} — {state} "
            f"({group.get('points_earned')}/{group.get('points_available')})</h4>"
            "<table><thead><tr><th>Test</th><th>Result</th><th>Time</th><th>Details</th></tr></thead>"
            f"<tbody>{''.join(tests)}</tbody></table>"
        )
    return "".join(sections) or "<p>No detailed test results were recorded.</p>"


def _submission_html(question: Mapping[str, Any]) -> str:
    submission = question.get("submission")
    if submission is None:
        return "<p>No accepted submission.</p>"
    files = []
    for file_item in submission.get("files", []):
        truncated = " <strong>(truncated in report)</strong>" if file_item.get("truncated") else ""
        files.append(
            f"<h4><code>{html.escape(str(file_item.get('path')))}</code>{truncated}</h4>"
            f"{_code_block(file_item.get('content'), empty='<source content not embedded>')}"
            f"<p class=\"muted\">SHA-256: <code>{html.escape(str(file_item.get('object_digest')))}</code></p>"
        )
    return (
        f"<p>Graded submission #{submission.get('sequence')} at {html.escape(str(submission.get('created_at')))}.</p>"
        + "".join(files)
    )


def _solution_html(question: Mapping[str, Any]) -> str:
    solution = question.get("solution")
    if solution is None:
        return "<p>No authored solution material is available for this question.</p>"
    parts = []
    explanation = solution.get("explanation")
    if explanation:
        parts.append(markdown_to_html(str(explanation.get("content", ""))))
    for reference in solution.get("reference_files", []):
        parts.append(
            f"<h4>Reference implementation: <code>{html.escape(str(reference.get('path')))}</code></h4>"
            f"{_code_block(reference.get('content'))}"
        )
    return "".join(parts)


def _feedback_list(items: Sequence[object], *, empty: str) -> str:
    return "".join(f"<li>{html.escape(str(item))}</li>" for item in items) or f"<li>{empty}</li>"


def render_report_html(document: Mapping[str, Any]) -> str:
    attempt = document["attempt"]
    grade = document.get("grade")
    feedback = document.get("feedback", {})
    toolchain = attempt.get("toolchain", {})
    image_metadata = toolchain.get("image", {})
    tool_items = (
        "".join(
            f"<li><strong>{html.escape(name)}</strong>: {html.escape(str(metadata.get('version', 'unknown')))}</li>"
            for name, metadata in sorted(toolchain.get("tools", {}).items())
        )
        or "<li>not recorded</li>"
    )
    score_html = "<p>Automatic grade not available.</p>"
    if grade:
        score = grade["score"]
        score_html = (
            f"<p class=\"score\"><strong>Automatic score:</strong> {score['earned']}/"
            f"{score['automatically_available']} <span>(paper total {score['total']})</span></p>"
            f"<p><strong>Not automatically assessed:</strong> {score['not_automatically_assessed']} points</p>"
        )
    hurdle_items = "<li>none</li>"
    if grade and grade["hurdles"]:
        hurdle_items = "".join(
            f"<li>{html.escape(hurdle['label'])}: {'PASS' if hurdle['passed'] else 'FAIL'}</li>"
            for hurdle in grade["hurdles"]
        )
    submission_items = (
        "".join(
            f"<li><code>{html.escape(str(item.get('question_id')))}</code> "
            f"#{item.get('sequence')} — <code>{html.escape(str(item.get('manifest_digest')))}</code></li>"
            for item in document.get("submissions", [])
        )
        or "<li>none</li>"
    )

    question_sections = []
    question_nav_items = []
    questions = document.get("questions", [])
    if not questions and grade:
        questions = [
            {
                "number": index,
                "id": item["id"],
                "title": item["title"],
                "points": item.get("total_points", item.get("automatic_points")),
                "tags": [],
                "prompt_markdown": "",
                "evaluation": item,
                "submission": item.get("submission"),
                "solution": None,
            }
            for index, item in enumerate(grade.get("questions", []), start=1)
        ]
    for question in questions:
        number = question.get("number")
        question_id = html.escape(str(question.get("id", number)), quote=True)
        evaluation = question.get("evaluation")
        state = (
            "NOT SUBMITTED"
            if question.get("submission") is None
            else (
                "NOT GRADED"
                if evaluation is None
                else ("PASS" if evaluation.get("passed") else "NEEDS WORK")
            )
        )
        earned = "—" if evaluation is None else evaluation.get("points_earned")
        available = "—" if evaluation is None else evaluation.get("automatic_points")
        tags = "".join(f'<span class="badge">{html.escape(str(tag))}</span>' for tag in question.get("tags", []))
        question_nav_items.append(
            f'<a href="#report-question-{question_id}">Q{number}. '
            f"{html.escape(str(question.get('title')))}</a>"
        )
        question_sections.append(
            f'<section class="exam-section report-question" id="report-question-{question_id}">'
            '<header class="section-heading">'
            f"<h2>Q{number}. {html.escape(str(question.get('title')))} "
            f"<small>({question.get('points')} marks)</small></h2>"
            f"<p><strong>{state}</strong> · automatic points {earned}/{available}</p></header>"
            f"<p>{tags}</p>"
            '<details class="report-detail"><summary>Question requirements</summary>'
            f"{markdown_to_html(str(question.get('prompt_markdown', '')))}</details>"
            '<details class="report-detail" open><summary>Submitted answer</summary>'
            f"{_submission_html(question)}</details>"
            '<details class="report-detail" open><summary>Evaluation details</summary>'
            f"{_test_details(evaluation)}</details>"
            '<details class="report-detail"><summary>Worked solution and reference implementation</summary>'
            f"{_solution_html(question)}</details>"
            "</section>"
        )

    identity = f"{attempt.get('profile', '')} {attempt.get('course', '')} {attempt.get('image', '')}"
    course = str(
        attempt.get("course") or ("COMP1521" if "1521" in identity else "COMP1511")
    )
    profile = str(attempt.get("profile", ""))
    theme_class = course_theme_class(profile, course)
    navbar = course_navbar(
        course=course,
        home_url="#summary",
        links=(
            '<a href="#summary">Summary</a>'
            '<details class="nav-menu"><summary>Questions</summary>'
            f'<div class="nav-menu-items">{"".join(question_nav_items)}</div></details>'
        ),
        status=f'<span class="badge">{html.escape(str(attempt["state"]))}</span>',
    )
    hero_score = "Automatic grade not available"
    if grade:
        score = grade["score"]
        hero_score = (
            f"Automatic score {score['earned']}/{score['automatically_available']} "
            f"· paper total {score['total']}"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>CSEExamTTY report {html.escape(attempt["id"])}</title>
{theme_style()}
<style>
.score {{ font-size:1.35rem; }} .score span {{ color:var(--muted); font-size:.9rem; }}
.summary-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:1rem; }}
.summary-grid .card-body {{ height:100%; }}
.report-question {{ scroll-margin-top:5rem; }}
.report-question .section-heading small {{ color:var(--muted); font-size:60%; font-weight:400; }}
.report-question pre {{ max-height:34rem; }}
.result-pass {{ color:#176b35; font-weight:700; }} .result-wrong_output,.result-wrong_exit_status,.result-compile_error,.result-runtime_error,.result-timeout,.result-output_limit,.result-internal_error {{ color:#a12622; font-weight:700; }}
</style>
</head>
<body class="{theme_class}">
{navbar}
<main class="container" aria-label="Content">
<header class="exam-hero">
<p class="text-muted text-uppercase"><strong>Local CSEExamTTY practice examination result</strong></p>
<h1>{html.escape(course)} attempt report</h1>
<p class="lead">{html.escape(str(attempt['pack']))}<br>{html.escape(hero_score)}</p>
<p class="text-muted">Candidate {html.escape(str(attempt.get('candidate_id') or 'practice user'))} · not an official UNSW mark</p>
</header>
<div class="alert alert-warning"><p>{html.escape(document["notice"])}</p></div>
<section class="exam-section" id="summary">
<header class="section-heading"><h2>Attempt summary</h2></header>
<dl>
<dt>Attempt</dt><dd><code>{html.escape(attempt["id"])}</code></dd>
<dt>Pack</dt><dd>{html.escape(attempt["pack"])}</dd>
<dt>Candidate</dt><dd>{html.escape(str(attempt.get("candidate_id") or "practice user"))}</dd>
<dt>State</dt><dd>{html.escape(attempt["state"])}</dd>
<dt>Mode</dt><dd>{html.escape(attempt["mode"])}</dd>
<dt>Image</dt><dd><code>{html.escape(attempt["image"])}</code></dd>
<dt>Image ID</dt><dd><code>{html.escape(str(image_metadata.get("id", "not recorded")))}</code></dd>
</dl>
{score_html}
<h3>Hurdles</h3><ul>{hurdle_items}</ul>
<h3>Accepted submission history</h3><ul>{submission_items}</ul>
</section>
<section class="summary-grid">
<div class="card"><div class="card-body"><h2>What went well</h2><ul>{_feedback_list(feedback.get("strengths", []), empty="No automatic strengths identified yet.")}</ul></div></div>
<div class="card"><div class="card-body"><h2>What still needs work</h2><ul>{_feedback_list(feedback.get("needs_work", []), empty="No automatic weaknesses identified.")}</ul></div></div>
</section>
<section class="exam-section"><header class="section-heading"><h2>Final recommendations</h2></header><ol>{_feedback_list(feedback.get("recommendations", []), empty="No recommendations available.")}</ol></section>
<section class="exam-section"><header class="section-heading"><h2>Recorded toolchain</h2></header><ul>{tool_items}</ul></section>
<h1 id="questions">Questions</h1>
{''.join(question_sections)}
<p class="text-muted text-uppercase" style="text-align:center"><strong>— End of local report. —</strong></p>
</main>
</body>
</html>
"""


def write_reports(root: Path, attempt_id: str, document: Mapping[str, Any]) -> tuple[Path, Path]:
    json_path = root / f"{attempt_id}.json"
    html_path = root / f"{attempt_id}.html"
    atomic_write(json_path, json.dumps(document, indent=2, sort_keys=True).encode() + b"\n")
    atomic_write(html_path, render_report_html(document).encode())
    return json_path, html_path
