# AI Prompt Guide

## Tech Stack & Constraints

- **Python**: 3.12+ (standard alpine runtime).
- **Web Framework**: Django 5.2.4 + django-filter 25.1 + django-compressor 4.5.1 + WhiteNoise 6.9.0.
- **Production Server**: Gunicorn 23.0.0.
- **Assets**: CSS minified via django-compressor. No custom frontend frameworks.
- **DB**: SQLite for local environment; external engine required for stateless Cloud Run staging.

## Coding Conventions

- **PEP 8 Rules**: Strictly follow PEP 8 styling conventions.
- **Explicit Routes**: Register URLs utilizing namespaced paths (`app_name = 'persinfo'`).
- **Templates**: Standard HTML templates must inherit `persinfo/base.html` or `base.html`. Must provide explicit `meta_description` block.
- **No Inline Styles**: Move any CSS style definitions to `style.css`.
- **View Signatures**: Provide standard type hints and clean docstrings for all custom views.

## Token Optimization Rules

- **Zero-Write Unchanged Code**: Do NOT rewrite files or blocks that did not change.
- **Targeted Code Replacements**: Use code replacement tools rather than recreating full files.
- **Skeletal Code Placeholders**: Use clear comments like `// ... existing code ...` or `# ... unchanged ...` for unaffected areas.
