import os
import shutil
from pathlib import Path
import yaml

CHILD_REPO = Path("child-repo")
TARGET_DOCS = Path("docs")
MKDOCS_YML = Path("mkdocs.yml")

def copy_md_files():
    copied = []
    for file in CHILD_REPO.rglob("*.md"):
        relative_path = file.relative_to(CHILD_REPO)
        dest_path = TARGET_DOCS / relative_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, dest_path)
        copied.append(dest_path.relative_to(TARGET_DOCS))
    return copied

def build_nav(files):
    nav = {}

    for path in files:
        parts = list(path.parts)
        current = nav
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        title = path.stem.replace("-", " ").title()
        current[title] = str(path).replace("\\", "/")

    def convert(nav_dict):
        nav_list = []
        for k, v in nav_dict.items():
            if isinstance(v, dict):
                nav_list.append({k: convert(v)})
            else:
                nav_list.append({k: v})
        return nav_list

    return convert(nav)

def write_mkdocs_yml(nav):
    content = {
        "site_name": "My Project Docs",
        "theme": {
            "name": "material",
            "features": ["navigation.tabs"]
        },
        "nav": nav
    }

    with open(MKDOCS_YML, "w") as f:
        yaml.dump(content, f, sort_keys=False)

if __name__ == "__main__":
    print("📂 Copying .md files from child-repo...")
    md_files = copy_md_files()
    print("🧭 Generating navigation...")
    nav = build_nav(md_files)
    print("📝 Writing mkdocs.yml...")
    write_mkdocs_yml(nav)
    print("✅ Done.")
