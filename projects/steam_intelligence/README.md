# steam_intelligence

Data Engineering and Analytics platform for Steam games.

---

## Dataset

Describe dataset.

---

## Objectives

- Objective 1
- Objective 2

---

## Structure

- `src/domain/` — entities and business rules, no I/O.
- `src/application/use_cases/` — ETL/orchestration steps (start here).
- `src/infrastructure/` — Postgres repositories, extractors, external services.
- `src/interfaces/` — CLI (`main.py`), and later API/dashboard entry points.
- `data/`, `models/`, `reports/`, `notebooks/` — generated artifacts, gitignored except structure.
- `tests/unit/`, `tests/integration/`

---

## Setup

```bash
pip install -e ../../shared
pip install -e .
cp .env.example .env
```

## Run

```bash
python main.py
```

---

## Technologies

- Python
- Pandas
- Numpy

---

## Author

Facu