## Usage

Take a look in [our sample project](./sample-docs) for an example implementation, or see [what it looks like after running `mkdocs build`](https://backstage.github.io/mkdocs-monorepo-plugin/monorepo-example/).

In general, this plugin introduces the `!include` syntax in your Mkdocs navigation structure and then merges them together.

```yaml
# /mkdocs.yml
site_name: Cats API

nav:
  - Intro: "index.md"
  - Authentication: "authentication.md"
  - API:
      - v1: "!include ./v1/mkdocs.yml"
      - v2: "!include ./v2/mkdocs.yml"

plugins:
  - monorepo
```

```yaml
# /src/v1/mkdocs.yml
site_name: versions/v1

nav:
  - Reference: "reference.md"
  - Changelog: "changelog.md"
```

```yaml
# /src/v2/mkdocs.yml
site_name: versions/v2

nav:
  - Migrating to v2: "migrating.md"
  - Reference: "reference.md"
  - Changelog: "changelog.md"
```

#### Example Source Filetree

```terminal
$ tree .

├── docs
│   ├── authentication.md
│   └── index.md
├── mkdocs.yml
├── v1
│   ├── docs
│   │   ├── changelog.md
│   │   └── reference.md
│   └── mkdocs.yml
└── v2
    ├── docs
    │   ├── changelog.md
    │   ├── migrating.md
    │   └── reference.md
    └── mkdocs.yml

5 directories, 10 files
```
