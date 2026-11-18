# Project documents

| Folder | Content |
|---|---|
| `en/` | Markdown sources, English |
| `ar/` | Markdown sources, Arabic |
| `pdf/en/`, `pdf/ar/` | Generated PDFs (do not edit) |
| `build/` | Generated HTML (temporary, can be git-ignored) |

- `00_Project_Master_Document` — the full project, for everyone.
- `01`–`06` — one document per role.

**To update:** edit the Markdown in `en/` and `ar/` (keep both in sync), then run:

```
pip install markdown
python docs/build.py
```

Needs Microsoft Edge or Google Chrome installed (used to print the PDFs, with correct Arabic rendering).
