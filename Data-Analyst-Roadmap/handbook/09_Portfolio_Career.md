# 09 · Portfolio & Career

*Part 9 of [The Complete Data Analyst & Data Science Roadmap](00_Table_of_Contents.md) · Previous: [08. Machine Learning](08_Machine_Learning.md)*

> 💡 **What you'll be able to do after this chapter**
> Package everything from Chapters 1–8 into a portfolio and job search that actually converts — Git hygiene, a resume that reads like impact instead of tasks, interview prep, and a freelancing on-ramp if you want one.

---

## 9.1 Git & GitHub

```bash
git init
git add .
git commit -m "Add customer churn analysis: SQL extraction + Python EDA"
git remote add origin <your-repo-url>
git push -u origin main
```

> ✅ **Best practice**
> Commit in meaningful chunks with messages that describe *why*, not "update file" — a hiring manager skimming your commit history is silently evaluating how you'll work on their team. This is the same discipline this handbook's own [`CHANGELOG.md`](../CHANGELOG.md) models.

## 9.2 README & Project Structure

Every project ([Chapter 07](07_Professional_Projects.md)) needs a README that a recruiter can read in 60 seconds and understand: **What was the business problem, what did you do, what did you find.** Lead with a screenshot of the dashboard or a key chart — not a wall of text.

> ⚠️ **Common mistake**
> A GitHub profile with 15 tutorial-following repos ("Titanic Notebook #1") and zero finished, narrated projects. Three complete projects with a real business framing (per [Chapter 07](07_Professional_Projects.md)) beat fifteen unfinished ones, every time.

## 9.3 LinkedIn & Resume

**Resume bullet formula:** `[Action] + [what you analyzed/built] + [quantified business impact]`

| Weak | Strong |
|---|---|
| "Used SQL and Python to analyze sales data" | "Identified a $180k/year revenue leak in a discount-stacking bug using SQL cohort analysis; recommendation adopted by Finance" |
| "Built Power BI dashboards" | "Built an executive Power BI dashboard adopted by 3 regional teams, replacing 6 hours/week of manual reporting" |

> ✅ **Best practice**
> Every bullet should survive the question "so what?" If it doesn't end in an outcome a business person cares about, rewrite it.

## 9.4 Interview Questions

**SQL round** (see also [Chapter 04](04_SQL.md)):
- Write a query to find the second-highest salary per department.
- Explain the difference between `WHERE` and `HAVING`.
- Given two tables, write a query to find customers with no orders.

**Python round** (see also [Chapter 05](05_Python.md)):
- Given a messy DataFrame, walk through your cleaning approach out loud.
- Explain `.groupby()` vs. a pivot table — when would you use each?

**Case study / business round:**
- "Weekly active users dropped 10% last week — walk me through how you'd investigate."
- Practice structuring your answer: clarify the metric definition → check for data issues → segment (by platform, geography, cohort) → form and test a hypothesis → recommend next steps.

**ML round** (see also [Chapter 08](08_Machine_Learning.md)):
- Precision vs. Recall — when do you optimize for one over the other?
- How do you know if a model is overfitting?

Track your own applications and questions in the [Notion Interview Tracker](../notion/08_Interview_Tracker.md).

## 9.5 Freelancing (Fiverr, Upwork)

Freelance data work is a legitimate way to build portfolio *and* income while job-hunting:

- Start with small, well-scoped gigs: "clean and analyze this dataset," "build me a 3-page Power BI dashboard."
- Price by the deliverable, not the hour, once you have 2-3 reviews.
- Every freelance project is a portfolio project — apply the [Chapter 07](07_Professional_Projects.md) structure to it too.

> ⚠️ **Common mistake**
> Underpricing to win the first gig, then staying underpriced forever. Price low for your first 2-3 reviews only, then raise rates — reviews are the asset you're actually buying at that stage.

## 9.6 Learning Timelines

| Track | Pace | Rough chapter pacing |
|---|---|---|
| **6 months** (intensive, ~25-30 hrs/wk) | Ch.01–03: 2 wks · SQL: 4 wks · Python: 5 wks · Power BI: 3 wks · Projects: 6 wks · ML: 4 wks · Portfolio/Job search: ongoing from month 4 |
| **12 months** (balanced, ~12-15 hrs/wk) | Same order, roughly double the time per phase, with 2 projects running in parallel with each new skill |
| **18 months** (part-time, ~6-8 hrs/wk) | Same order, one topic at a time, minimum 1 project shipped per quarter |

Weekly/daily schedule templates are in the [Notion Learning Calendar](../notion/04_Learning_Calendar.md).

## 9.7 Senior Engineer Advice

> 🏢 **From the trenches**
> - "The best analysts I've hired weren't the best at SQL — they were the best at asking 'is this the right question?' before writing any query."
> - "Your first six months on the job, over-communicate assumptions. A wrong number nobody questioned is worse than a slow number everyone trusts."
> - "Don't wait for permission to be curious about a metric that looks off. That instinct is the actual job."

---

## Chapter Summary

- Git/GitHub hygiene and a README that leads with business impact are part of the deliverable, not an afterthought.
- Resume bullets should survive "so what?" — quantify business impact, not just tools used.
- Prepare for four interview lanes: SQL, Python, business case, and (if relevant) ML.
- Freelancing is a legitimate parallel path — treat every gig like a portfolio project.
- Pick a timeline (6/12/18 months) that matches your real available hours, not your ambition.

**This completes the core handbook.** Return to the [Table of Contents](00_Table_of_Contents.md) · Continue to the [10 portfolio projects](../projects/) to apply everything.
