"""
Automates creating the Notion workspace from the Markdown files in this folder,
using the official Notion API. Builds the same hierarchy described in
00_Home.md: one parent page with 9 child pages underneath it.

Setup (one-time):
  1. Create an internal integration at https://www.notion.so/my-integrations
     and copy its "Internal Integration Secret".
  2. In Notion, create (or pick) a page that will act as the workspace root,
     then click "..." -> "Add connections" -> select your integration, so it
     can create pages inside it. Copy that page's ID from its URL (the 32-char
     string after the last "-").
  3. pip install notion-client

Usage:
  set NOTION_TOKEN=secret_xxx            (Windows: $env:NOTION_TOKEN="secret_xxx")
  set NOTION_PARENT_PAGE_ID=xxxxxxxxxxxx
  python notion/build_notion_workspace.py

This performs a lightweight Markdown -> Notion-blocks conversion: headings,
paragraphs, bullet lists, blockquotes (callouts), tables, and code blocks.
It is intentionally simple — good enough to stand up the workspace structure
and content in one pass; polish formatting afterward in Notion itself.
"""
import os
import re
import sys
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    sys.exit("Run: pip install notion-client")

NOTION_DIR = Path(__file__).resolve().parent

PAGE_ORDER = [
    ("00_Home.md", None),  # root page, created first
    ("01_Chapter_Index.md", "00_Home.md"),
    ("02_Progress_Tracker.md", "00_Home.md"),
    ("03_Checklist.md", "00_Home.md"),
    ("04_Learning_Calendar.md", "00_Home.md"),
    ("05_Project_Database.md", "00_Home.md"),
    ("06_Dataset_Database.md", "00_Home.md"),
    ("07_Exercise_Database.md", "00_Home.md"),
    ("08_Interview_Tracker.md", "00_Home.md"),
    ("09_Resources.md", "00_Home.md"),
]


def rich_text(content: str):
    return [{"type": "text", "text": {"content": content[:2000]}}]


def md_line_to_block(line: str):
    line = line.rstrip()
    if not line.strip():
        return None
    if line.startswith("### "):
        return {"object": "block", "type": "heading_3",
                "heading_3": {"rich_text": rich_text(line[4:])}}
    if line.startswith("## "):
        return {"object": "block", "type": "heading_2",
                "heading_2": {"rich_text": rich_text(line[3:])}}
    if line.startswith("# "):
        return {"object": "block", "type": "heading_1",
                "heading_1": {"rich_text": rich_text(line[2:])}}
    if line.startswith("> "):
        return {"object": "block", "type": "callout",
                "callout": {"rich_text": rich_text(line[2:]), "icon": {"emoji": "💡"}}}
    if line.startswith(("- ", "* ")):
        text = line[2:]
        checked = None
        if text.startswith("[ ] "):
            return {"object": "block", "type": "to_do",
                    "to_do": {"rich_text": rich_text(text[4:]), "checked": False}}
        if text.startswith("[x] "):
            return {"object": "block", "type": "to_do",
                    "to_do": {"rich_text": rich_text(text[4:]), "checked": True}}
        return {"object": "block", "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": rich_text(text)}}
    if line.startswith("|"):
        return None  # tables handled separately (see convert_markdown)
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": rich_text(line)}}


def convert_markdown(md_text: str):
    blocks = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
            # naive markdown table -> Notion table block
            header_cells = [c.strip() for c in line.strip("|").split("|")]
            rows = [header_cells]
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip("|").split("|")])
                j += 1
            width = len(header_cells)
            table_block = {
                "object": "block", "type": "table",
                "table": {
                    "table_width": width, "has_column_header": True, "has_row_header": False,
                    "children": [
                        {"object": "block", "type": "table_row",
                         "table_row": {"cells": [rich_text(c) for c in row[:width]]}}
                        for row in rows
                    ],
                },
            }
            blocks.append(table_block)
            i = j
            continue
        block = md_line_to_block(line)
        if block:
            blocks.append(block)
        i += 1
    return blocks[:100]  # Notion API caps children per request; extend with pagination if needed


def main():
    token = os.environ.get("NOTION_TOKEN")
    parent_id = os.environ.get("NOTION_PARENT_PAGE_ID")
    if not token or not parent_id:
        sys.exit("Set NOTION_TOKEN and NOTION_PARENT_PAGE_ID environment variables first (see docstring).")

    notion = Client(auth=token)
    created_ids = {}

    for fname, parent_file in PAGE_ORDER:
        path = NOTION_DIR / fname
        md = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
        title = title_match.group(1) if title_match else fname
        blocks = convert_markdown(md)

        parent = (
            {"type": "page_id", "page_id": parent_id}
            if parent_file is None
            else {"type": "page_id", "page_id": created_ids[parent_file]}
        )
        page = notion.pages.create(
            parent=parent,
            properties={"title": {"title": [{"type": "text", "text": {"content": title}}]}},
            children=blocks,
        )
        created_ids[fname] = page["id"]
        print(f"  [ok] {fname} -> {page['url']}")

    print("\nDone. Open the parent page in Notion to see the full hierarchy.")


if __name__ == "__main__":
    main()
