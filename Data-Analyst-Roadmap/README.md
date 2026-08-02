# The Complete Data Analyst & Data Science Roadmap

> A premium, company-grade handbook that takes you from beginner/intermediate to a professional Data Analyst — with a runway into Data Science. Written the way a Senior Data Scientist mentors a junior on the job: practical, workflow-first, real-company examples over theory.

Status: ✅ **Core handbook complete.** All 9 chapters, the dataset catalog, all 10 portfolio projects, a printable PDF, and Notion workspace automation are done. Remaining work (per-chapter exercise sets, per-project code/dashboards) is tracked in [progress/PROGRESS.md](progress/PROGRESS.md). See [CHANGELOG.md](CHANGELOG.md) for the full build history.

---

## Why this handbook is different

Most "learn data analytics" material follows the **Kaggle workflow**: download a clean CSV, run `.describe()`, make a chart, done.

This handbook follows the **real company workflow**:

```
Users → Applications → Operational Database → ETL/ELT → Data Warehouse
      → SQL → Python → Power BI → Business Decision → Machine Learning → Deployment
```

Every chapter is anchored to where it sits in that pipeline, and every concept answers: *"What does this look like inside a real company?"*

## How the repository is organized

| Folder | What's in it |
|---|---|
| [`handbook/`](handbook/) | The 9-part core handbook, chapter by chapter |
| [`notion/`](notion/) | Notion-ready workspace: Home, Progress Tracker, Checklist, Calendar, and 5 databases |
| [`exercises/`](exercises/) | Warm-up → Practice → Challenge → Mini Project → Solutions, per chapter |
| [`datasets/`](datasets/) | Curated dataset briefs per chapter (difficulty, business context, deliverables, links) |
| [`projects/`](projects/) | 10 full portfolio-grade, company-style projects |
| [`assets/`](assets/) | Diagrams (Mermaid), icons, screenshots, illustrations, images |
| [`references/`](references/) | Books, YouTube channels, glossary, external docs |
| [`pdf/`](pdf/) | Compiled, printable version of the handbook |
| [`progress/`](progress/) | Live progress tracker mirrored from `notion/02_Progress_Tracker.md` |

## Start reading

Begin at the [Table of Contents](handbook/00_Table_of_Contents.md).

## Importing into Notion

Two options — see [`notion/NOTION_AI_PROMPT.md`](notion/NOTION_AI_PROMPT.md):
- **Automated:** run [`notion/build_notion_workspace.py`](notion/build_notion_workspace.py) with a Notion integration token to create the entire page hierarchy via the API.
- **Manual:** import `notion/00_Home.md` as your top-level page, then import every other file in [`notion/`](notion/) as sub-pages of it — or paste the included Notion AI prompt to have Notion's own AI scaffold it for you.

## Building the printable PDF

```bash
pip install markdown
python pdf/build_pdf.py
```

See [`pdf/README.md`](pdf/README.md) for details and engine fallbacks. Current build: [`pdf/The_Complete_Data_Analyst_Roadmap.pdf`](pdf/The_Complete_Data_Analyst_Roadmap.pdf).

## Contributing / continuing this project

This handbook is built incrementally, one chapter at a time, to keep every chapter production-ready rather than shipping a rough draft of everything at once. If you're picking this up:

1. Check [progress/PROGRESS.md](progress/PROGRESS.md) for the next unstarted chapter.
2. Follow the structure and cross-referencing pattern already established in completed chapters.
3. Update [CHANGELOG.md](CHANGELOG.md), [progress/PROGRESS.md](progress/PROGRESS.md), this README's status line, and `notion/01_Chapter_Index.md` / `notion/02_Progress_Tracker.md` after finishing a chapter.
