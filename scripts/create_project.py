import shutil
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

WORKSPACE = Path(__file__).resolve().parent.parent

TEMPLATES = WORKSPACE / "templates"

PROJECTS = WORKSPACE / "projects"


# ============================================================
# FUNCTIONS
# ============================================================

def choose_template():

    templates = sorted(
        [folder for folder in TEMPLATES.iterdir() if folder.is_dir()]
    )

    print("\nAvailable templates:\n")

    for index, template in enumerate(templates, start=1):
        print(f"{index}. {template.name}")

    while True:

        option = input("\nTemplate: ")

        try:

            option = int(option)

            if 1 <= option <= len(templates):
                return templates[option - 1]

        except ValueError:
            pass

        print("Invalid option.")


def ask_project_name():

    while True:

        name = input("\nProject name: ").strip()

        if not name:
            continue

        name = name.lower().replace(" ", "_")

        destination = PROJECTS / name

        if destination.exists():

            print("Project already exists.")

            continue

        return name


IGNORED_PATTERNS = shutil.ignore_patterns(
    ".ruff_cache", "__pycache__", "*.pyc", ".git"
)


def copy_template(template: Path, project_name: str):

    destination = PROJECTS / project_name

    shutil.copytree(template, destination, ignore=IGNORED_PATTERNS)

    return destination


def replace_placeholders(project_path: Path, project_name: str):

    replacements = {
        "{{PROJECT_NAME}}": project_name
    }

    for file in project_path.rglob("*"):

        if file.suffix not in {
            ".py",
            ".md",
            ".txt",
            ".toml",
            ".yaml",
            ".yml",
            ".json",
            ".env"
        }:
            continue

        try:

            text = file.read_text(encoding="utf-8")

            for key, value in replacements.items():
                text = text.replace(key, value)

            file.write_text(text, encoding="utf-8")

        except Exception:
            pass


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 50)
    print("DATA ANALYTICS PROJECT CREATOR")
    print("=" * 50)

    project_name = ask_project_name()

    template = choose_template()

    project = copy_template(template, project_name)

    replace_placeholders(project, project_name)

    print("\nProject created successfully.\n")

    print(project)


if __name__ == "__main__":
    main()