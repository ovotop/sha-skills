#!/usr/bin/env python3
"""check_plain.py — deterministic zh/en controlled-writing linter for the sha-plain-docs skill.

Usage:
    python3 check_plain.py [PATH] [--text TEXT] [--lang zh|en] [--json]
                           [--source FILE] [--greenfield] [--avoid-words PATH]

Exit codes: 0 = no violations, 1 = at least one violation, 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CJK_RANGES = ((0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0xF900, 0xFAFF), (0x20000, 0x2FFFF))
CJK_CLASS = r"\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff"
STRONG_ZH = ["一定", "绝对", "必定", "必然", "肯定", "显然", "无疑", "确实", "确定", "从不", "总是", "永远"]
STRONG_EN = ["always", "never", "definitely", "certainly", "obviously", "proven"]
NORMATIVE_ZH = ["必须", "不得", "禁止"]
NORMATIVE_EN = ["must"]
SOURCE_STEMS = ["根据", "依据", "来自", "显示", "表明", "报告", "文档", "监控", "日志", "测试", "实验", "测量", "数据", "统计", "反馈", "引用", "据"]
DROPPED_MARKERS = ["仅", "不得", "除非", "只有", "除外", "注意", "警告", "限制", "不能", "禁止"]

CODE_SPAN_RE = re.compile(r"`+[^`\n]*`+")
URL_RE = re.compile(r"https?://[^\s,，。；：？！()<>]+|(?:^|\s)(?:/[\w.\-]+){2,}")
HEADING_RE = re.compile(r"^#{1,6}\s+")
SENT_SPLIT = re.compile(r"[。！？；]+")
EN_SENT_SPLIT = re.compile(r"[.!?;]+")
CLAUSE_SPLIT = re.compile(r"[，、]")
SOURCE_RE = re.compile(
    r"(?:[（(][^）)]{0,40}(?:" + "|".join(SOURCE_STEMS) + r")[^）)]{0,40}[）)])"
    r"|(?:" + "|".join(SOURCE_STEMS) + r")\s*\S"
    r"|见\s*[「『\"']"
)
STRONG_EN_RE = re.compile(r"\b(?:" + "|".join(STRONG_EN) + r")\b", re.IGNORECASE)
NORMATIVE_EN_RE = re.compile(r"\b(?:" + "|".join(NORMATIVE_EN) + r")\b", re.IGNORECASE)


def is_cjk(ch: str) -> bool:
    if not ch:
        return False
    code = ord(ch)
    return any(low <= code <= high for low, high in CJK_RANGES)


def mask_line(line: str) -> str:
    chars = list(line)
    for pattern in (CODE_SPAN_RE, URL_RE):
        for match in pattern.finditer(line):
            for index in range(match.start(), match.end()):
                chars[index] = " "
    return "".join(chars)


def char_len(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def word_len(text: str) -> int:
    return len(text.split())


def load_entries(path: Path):
    literal, regex, allowlist = [], [], []
    section = ""
    in_allowlist = False
    for raw in path.read_text(encoding="utf-8").split("\n"):
        line = raw.rstrip()
        if line.startswith("### "):
            in_allowlist = line.startswith("### 允许清单")
            continue
        if line.startswith("## "):
            section = line[3:].strip()
            in_allowlist = False
            continue
        if not line.startswith("- "):
            continue
        head = line[2:].split("→", 1)[0].strip()
        if in_allowlist:
            allowlist.append(head)
            continue
        if "→" not in line:
            continue
        if head.startswith("/") and head.endswith("/") and len(head) > 1:
            regex.append((re.compile(head[1:-1]), section, head[1:-1]))
        else:
            literal.append((head, section))
    return literal, regex, allowlist


def apply_entries(entries, line_text, is_en, allow_intervals, lineno, findings):
    for pattern, section, label in entries[1]:
        if ("英文" in section) != is_en:
            continue
        for match in pattern.finditer(line_text):
            if _inside_allowlist(match.start(), match.end(), allow_intervals):
                continue
            findings.append(_finding("banned_word", "violation", lineno, match.group(0), f"禁用词「{label}」，请改为平实表达"))
    for label, section in entries[0]:
        if ("英文" in section) != is_en:
            continue
        needle = label
        haystack = line_text
        if is_en:
            needle, haystack = label.lower(), line_text.lower()
        start = haystack.find(needle)
        span = len(needle)
        while start != -1:
            if not _inside_allowlist(start, start + span, allow_intervals):
                findings.append(_finding("banned_word", "violation", lineno, line_text[start:start + span], f"禁用词「{label}」，请改为平实表达"))
            start = haystack.find(needle, start + 1)


def _inside_allowlist(start, end, intervals):
    return any(start >= low and end <= high for low, high in intervals)


def _allow_intervals(line_text, allowlist):
    intervals = []
    for word in allowlist:
        pos = line_text.find(word)
        while pos != -1:
            intervals.append((pos, pos + len(word)))
            pos = line_text.find(word, pos + 1)
    return intervals


def _finding(rule, severity, line, snippet, message):
    return {"rule": rule, "severity": severity, "line": line, "snippet": snippet, "message": message}


def collect_lines(text: str):
    lines = []
    front_seen = False
    in_front = False
    in_code = False
    ref_def_re = re.compile(r"^\[[^\]]+\]:\s+\S+")
    for number, raw in enumerate(text.split("\n"), start=1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_front = True
            lines.append({"no": number, "raw": raw, "skip": True})
            continue
        if in_front:
            if stripped == "---":
                in_front = False
            lines.append({"no": number, "raw": raw, "skip": True})
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            lines.append({"no": number, "raw": raw, "skip": True})
            continue
        if in_code or stripped.startswith("|") or not stripped or ref_def_re.match(stripped):
            lines.append({"no": number, "raw": raw, "skip": True})
            continue
        masked = mask_line(raw)
        measure = HEADING_RE.sub("", masked)
        lines.append({"no": number, "raw": raw, "masked": masked, "measure": measure, "skip": False})
    return lines


def check_sentence_length(lines, lang, findings):
    for item in lines:
        if item["skip"]:
            continue
        splitter = EN_SENT_SPLIT if lang == "en" else SENT_SPLIT
        for piece in splitter.split(item["measure"]):
            sentence = piece.strip()
            if not sentence:
                continue
            if lang == "en":
                count = word_len(sentence)
                if count > 25:
                    findings.append(_finding("sentence_too_long", "violation", item["no"], sentence, f"英文句子 {count} 词，超过 25 词上限，请拆分"))
                elif 20 <= count <= 25:
                    findings.append(_finding("sentence_needs_review", "info", item["no"], sentence, "需确认语义明确（20–25 词）"))
            else:
                count = char_len(sentence)
                if count > 40:
                    findings.append(_finding("sentence_too_long", "violation", item["no"], sentence, f"单句 {count} 字，超过 40 字上限，请拆分"))
                elif 30 <= count <= 39 and not CLAUSE_SPLIT.search(sentence):
                    findings.append(_finding("sentence_needs_review", "info", item["no"], sentence, "需确认语义明确（30–39 字）"))
                if CLAUSE_SPLIT.search(sentence):
                    for clause in CLAUSE_SPLIT.split(sentence):
                        clause = clause.strip()
                        if char_len(clause) > 20:
                            findings.append(_finding("clause_too_long", "violation", item["no"], clause, f"逗号构件 {char_len(clause)} 字，超过 20 字上限，请拆分"))
    return


def check_facts(lines, lang, greenfield, findings):
    previous = ""
    strong = STRONG_EN_RE if lang == "en" else None
    normative = NORMATIVE_EN_RE if lang == "en" else None
    for item in lines:
        if item["skip"]:
            continue
        splitter = EN_SENT_SPLIT if lang == "en" else SENT_SPLIT
        for piece in splitter.split(item["raw"]):
            sentence = piece.strip()
            if not sentence:
                continue
            norm_hits = [m.group(0) for m in normative.finditer(sentence)] if normative else [w for w in NORMATIVE_ZH if w in sentence]
            for hit in dict.fromkeys(norm_hits):
                findings.append(_finding("normative_modality", "warning", item["no"], sentence, f"规范型情态「{hit}」是要求而非事实断言，默认告警、不需要来源标记；不得新增原稿没有的要求"))
            hits = [m.group(0) for m in strong.finditer(sentence)] if strong else [w for w in STRONG_ZH if w in sentence]
            if hits:
                context = f"{sentence}\n{previous}\n{item['raw']}"
                if not SOURCE_RE.search(context):
                    severity = "warning" if greenfield else "violation"
                    rule = "strong_claim_without_source_greenfield" if greenfield else "strong_claim_without_source"
                    note = "需人工/LLM 复核：强断言缺少可核对来源" if greenfield else "强断言缺少可核对来源，请补充来源、降级语态或删除"
                    for hit in dict.fromkeys(hits):
                        findings.append(_finding(rule, severity, item["no"], sentence, f"{note}（{hit}）"))
            previous = sentence


def check_punctuation(lines, lang, findings):
    for item in lines:
        if item["skip"]:
            continue
        masked = item["masked"]
        for index, ch in enumerate(masked):
            if is_cjk(ch):
                after = masked[index + 1] if index + 1 < len(masked) else ""
                if after and after.isascii() and after.isalnum():
                    findings.append(_finding("missing_cjk_latin_space", "violation", item["no"], f"{ch}{after}", "中文与英文/数字之间请加一个空格"))


def normalize_for_compare(text: str) -> str:
    return "".join(ch for ch in text if is_cjk(ch) or ch.isalnum())


def check_source_diff(source_text, output_text, findings):
    src_lines = source_text.split("\n")
    normalized = normalize_for_compare("\n".join(src_lines))
    positions = []
    cursor = 0
    for number, raw in enumerate(src_lines, start=1):
        for marker in DROPPED_MARKERS:
            count = normalize_for_compare(raw).count(marker)
            positions.extend([(cursor + i, marker, number, raw) for i in range(count)])
        cursor += len(normalize_for_compare(raw))
    out_norm = normalize_for_compare(output_text)
    for marker in DROPPED_MARKERS:
        src_occurrences = [item for item in positions if item[1] == marker]
        kept = out_norm.count(marker)
        for index in range(kept, len(src_occurrences)):
            _, _, number, raw = src_occurrences[index]
            findings.append(_finding("dropped_warning", "violation", number, raw.strip(), f"删改对比（尽力而为）：原稿的警告/限制词「{marker}」在输出中消失"))


def run(args):
    text = args.text
    if args.path and text is not None:
        raise ValueError("不能同时提供 PATH 与 --text")
    if args.path:
        path = Path(args.path)
        if not path.is_file():
            raise ValueError(f"无法读取文件：{args.path}")
        text = path.read_text(encoding="utf-8")
    elif text is None:
        text = sys.stdin.read()

    word_list = Path(args.avoid_words) if args.avoid_words else Path(__file__).resolve().parent.parent / "references" / "avoid-words.md"
    if not word_list.is_file():
        raise ValueError(f"找不到词表：{word_list}")
    entries = load_entries(word_list)

    lines = collect_lines(text)
    findings = []
    check_sentence_length(lines, args.lang, findings)
    check_facts(lines, args.lang, args.greenfield, findings)
    check_punctuation(lines, args.lang, findings)
    for item in lines:
        if item["skip"]:
            continue
        apply_entries(entries, item["masked"], args.lang == "en", _allow_intervals(item["masked"], entries[2]), item["no"], findings)

    skipped = []
    if args.source:
        source_path = Path(args.source)
        if not source_path.is_file():
            raise ValueError(f"无法读取原稿：{args.source}")
        check_source_diff(source_path.read_text(encoding="utf-8"), text, findings)
    else:
        skipped.append("source_diff")
        findings.append(_finding("source_diff_skipped", "info", 1, "", "删改对比需 --source"))

    findings.sort(key=lambda f: (f["line"], f["rule"]))
    summary = {
        "violations": sum(1 for f in findings if f["severity"] == "violation"),
        "warnings": sum(1 for f in findings if f["severity"] == "warning"),
        "infos": sum(1 for f in findings if f["severity"] == "info"),
    }
    report = {
        "file": args.path or ("<text>" if args.text is not None else "<stdin>"),
        "lang": args.lang,
        "findings": findings,
        "summary": summary,
        "checks_skipped": skipped,
    }
    return report


def print_human(report, check_source):
    if not report["findings"]:
        print("no findings")
    if check_source:
        print("# 删改对比：尽力而为（仅检测显式警告标记词，不覆盖语义性删除）")
    for finding in report["findings"]:
        snippet = f" {finding['snippet']}" if finding["snippet"] else ""
        print(f"L{finding['line']}: [{finding['severity']}] {finding['rule']}{snippet} — {finding['message']}")
    summary = report["summary"]
    print(f"{summary['violations']} violations, {summary['warnings']} warnings, {summary['infos']} infos")
    if report["checks_skipped"]:
        print("checks_skipped: " + ", ".join(report["checks_skipped"]))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="check_plain.py", description="Deterministic zh/en controlled-writing linter.")
    parser.add_argument("path", nargs="?", help="document to check")
    parser.add_argument("--text", default=None, help="inline text instead of a file")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    parser.add_argument("--source", default=None, help="original draft, enables the dropped-warning diff")
    parser.add_argument("--greenfield", action="store_true", help="downgrade check_facts findings to warnings")
    parser.add_argument("--avoid-words", default=None, help="override the word list path")
    args = parser.parse_args(argv)

    try:
        report = run(args)
    except ValueError as error:
        print(f"usage error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report, bool(args.source))
    return 1 if report["summary"]["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
