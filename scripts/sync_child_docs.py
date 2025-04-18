# scripts/sync_child_docs.py

import os
import shutil
import yaml

CHILD_REPO = "child-repo"
DOCS_DIR = "docs"
MKDOCS_YML = "mkdocs.yml"

def find_md_files(base_path):
    md_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_path)
                md_files.append(rel_path)
    return md_files

def sync_docs():
    # Step 1: find all child .md files
    child_files = find_md_files(CHILD_REPO)

    # Step 2: remove previously synced .md files in docs/ not in child anymore
    docs_files = find_md_files(DOCS_DIR)
    for file in docs_files:
        if file.lower() == "readme.md":
            continue  # Keep the manually created one
        if file not in child_files:
            os.remove(os.path.join(DOCS_DIR, file))

    # Step 3: copy files from child to docs/
    for file in child_files:
        src = os.path.join(CHILD_REPO, file)
        dst = os.path.join(DOCS_DIR, file.lower())  # Normalize filenames
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

def update_mkdocs_yml():
    nav = [{"Home": "index.md"}]

    docs_files = sorted(find_md_files(DOCS_DIR))
    for file in docs_files:
        if file == "index.md":
            continue
        title = os.path.splitext(os.path.basename(file))[0].replace("-", " ").capitalize()
        nav.append({title: file})

    with open(MKDOCS_YML, "r") as f:
        config = yaml.safe_load(f)

    config["nav"] = nav

    with open(MKDOCS_YML, "w") as f:
        yaml.dump(config, f, sort_keys=False)

if __name__ == "__main__":
    sync_docs()
    update_mkdocs_yml()
