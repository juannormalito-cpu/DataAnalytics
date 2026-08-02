# Notion AI Execution Prompt

Two ways to stand up the Notion workspace — pick one.

---

## Option A — Automated (Notion API script)

Use [`build_notion_workspace.py`](build_notion_workspace.py) — it reads every `.md` file in this folder and creates the real Notion page hierarchy for you via the API. See the docstring at the top of that file for the 3 setup steps (integration token, parent page ID, `pip install notion-client`), then:

```bash
python notion/build_notion_workspace.py
```

## Option B — Manual, via Notion AI

If you'd rather not set up an API integration, paste the prompt below into Notion AI (open a blank page → type `/ask ai` or use the AI sidebar) and it will scaffold the same structure for you to then paste each `.md` file's content into.

> Paste everything between the lines into Notion AI:

---

**PROMPT START**

Create a Notion workspace page hierarchy for a learning resource called **"The Complete Data Analyst & Data Science Roadmap"**. Build one top-level page named **🏠 Home**, and under it, create these 9 sub-pages in this exact order, each with the given title, icon, and purpose (create the purpose as a short description/callout at the top of each page, then leave the rest blank for me to paste content into):

1. **📚 Chapter Index** — a table tracking the 9 handbook chapters (columns: #, Chapter, Status, Source file), status values Not Started / In Progress / Production-ready.
2. **🧭 Progress Tracker** — a database/table tracking chapter status, exercises, datasets linked, and diagrams per chapter, plus a second table tracking the 10 portfolio projects, plus a third table for infrastructure deliverables (repo scaffold, dataset catalog, PDF).
3. **✅ Checklist** — a set of to-do checklists grouped by skill area: Foundations, Databases, SQL, Python, Power BI, Machine Learning, Portfolio & Career.
4. **📅 Learning Calendar** — a page comparing 3 learning tracks (6-month intensive, 12-month balanced, 18-month part-time) plus a weekly schedule template table and a daily schedule template table.
5. **🗂️ Project Database** — a table of 10 portfolio projects with columns: #, Project, Difficulty, Stack, Status, Folder link.
6. **📊 Dataset Database** — a table of datasets used across the handbook with columns: Dataset, Chapter, Difficulty, Source link, Estimated time.
7. **🏋️ Exercise Database** — a table with one row per chapter and columns for Warm-up / Practice / Challenge / Mini Project / Solutions completion status.
8. **🎤 Interview Tracker** — a table with columns: Company, Role, Stage (Applied/Screen/Technical/Case Study/Onsite/Offer/Rejected), Date, Notes — set up as a Kanban board grouped by Stage.
9. **🔖 Bookmarks & Resources** — a table with columns: Type (Book/Channel/Docs/Cheat Sheet/Tool), Title, Chapter, Link.

Use Notion databases (not plain tables) wherever a "Status" or "Stage" column is involved, so I can build Board/Calendar views on top of them later. Use consistent icons (the emoji given above) on every page. Link every sub-page back to 🏠 Home at the top.

**PROMPT END**

---

After Notion AI builds the shell, copy the full content of each corresponding file in this folder (`00_Home.md` through `09_Resources.md`) into its matching page — the Markdown headings/tables/checkboxes paste cleanly into Notion's own blocks.
