# Assets

Visual assets for the handbook. Mermaid is used inline in chapter Markdown wherever possible (renders natively on GitHub, Notion via embed, and most static site generators). This folder holds everything Mermaid can't express.

| Folder | Contents |
|---|---|
| `diagrams/` | Exported architecture/ETL/schema diagrams (PNG/SVG) for chapters that need more than Mermaid, or Mermaid source files (`.mmd`) kept alongside chapters |
| `icons/` | Small icon assets used in callout boxes / role comparisons |
| `screenshots/` | Power BI, SQL tool, and cloud console screenshots referenced by chapters |
| `illustrations/` | Custom illustration prompts + generated images for section headers |
| `images/` | General-purpose images (covers, banners) |

## Illustration prompt convention

When a diagram exceeds what Mermaid can express, this repo stores a **prompt file** (`.prompt.md`) next to where the image will go, e.g. `illustrations/02_data_flow_hero.prompt.md`, describing exactly what to generate. This keeps the visual spec version-controlled even before the final image exists.
