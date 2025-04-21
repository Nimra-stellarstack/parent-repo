import os
import shutil
import yaml

CHILD_REPO_PATH = "child-repo"
DOCS_CHILD_PATH = "docs/child-repo"
MKDOCS_YML = "mkdocs.yml"

def ensure_docs_child_path():
    os.makedirs(DOCS_CHILD_PATH, exist_ok=True)

def copy_markdown_files():
    # Clean the child docs folder first to remove outdated files
    if os.path.exists(DOCS_CHILD_PATH):
        shutil.rmtree(DOCS_CHILD_PATH)
    os.makedirs(DOCS_CHILD_PATH, exist_ok=True)

    for root, dirs, files in os.walk(CHILD_REPO_PATH):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), CHILD_REPO_PATH)
                dest_path = os.path.join(DOCS_CHILD_PATH, rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Normalize README as lowercase
                if os.path.basename(file).lower() == "readme.md":
                    dest_path = os.path.join(os.path.dirname(dest_path), "readme.md")

                shutil.copy2(os.path.join(root, file), dest_path)

def build_nav_for_file(path):
    name = os.path.splitext(os.path.basename(path))[0].replace("-", " ").capitalize()
    return {name: path.replace("\\", "/")}

def load_existing_nav(yml_path):
    with open(yml_path, "r") as f:
        return yaml.safe_load(f)

def update_mkdocs_nav(existing):
    # Clear out any existing 'Child Docs' sections
    cleaned_nav = []
    for item in existing.get("nav", []):
        if isinstance(item, dict):
            key = list(item.keys())[0]
            if key != "Child Docs":
                cleaned_nav.append(item)
        else:
            cleaned_nav.append(item)

    # Collect child files into new nav entries
    child_nav = []
    for root, _, files in os.walk(DOCS_CHILD_PATH):
        for file in sorted(files):
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), "docs")
                child_nav.append(build_nav_for_file(rel_path))

    # Append cleaned original nav with fresh Child Docs
    cleaned_nav.append({"Child Docs": child_nav})
    existing["nav"] = cleaned_nav
    return existing

def write_updated_mkdocs(config):
    with open(MKDOCS_YML, "w") as f:
        yaml.dump(config, f, sort_keys=False)

def main():
    ensure_docs_child_path()
    copy_markdown_files()

    mkdocs_config = load_existing_nav(MKDOCS_YML)
    updated_config = update_mkdocs_nav(mkdocs_config)
    write_updated_mkdocs(updated_config)

    print("✅ Synced child repo markdown files into docs/child-repo and updated mkdocs.yml.")

if __name__ == "__main__":
    main()
