# Codebase Index

## System Architecture

```
+-------------------------------------------------------+
|                    GCP Cloud Run                      |
|                                                       |
|  +-------------------------------------------------+  |
|  |                 Docker Container                |  |
|  |                                                 |  |
|  |   +----------+      Gzip     +---------------+  |  |
|  |   | Gunicorn | <-----------> | Whitenoise /  |  |  |
|  |   +----------+               | django-       |  |  |
|  |        ^                     | compressor    |  |  |
|  |        |                     +---------------+  |  |
|  |        v                             |          |  |
|  |   +----------+                       v          |  |
|  |   |  Django  | --------------> static/staticfiles  |  |
|  |   |  (pers-  |                                  |  |
|  |   |   info)  |                                  |  |
|  |   +----------+                                  |  |
|  |     ^      ^                                    |  |
|  |     |      |                                    |  |
|  |     v      v                                    |  |
|  |  +----+  +------------+                         |  |
|  |  | DB |  | DB Cache   |                         |  |
|  |  |    |  | (shared    |                         |  |
|  |  |    |  |  SQLite3)  |                         |  |
|  |  +----+  +------------+                         |  |
|  +-------------------------------------------------+  |
+-------------------------------------------------------+
      SQLite3   (Local Disk)
```

## Directory Tree

```
F:\REpo\Website
├── Dockerfile
├── requirements.txt
├── manage.py
├── db.sqlite3
├── mainweb/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── persinfo/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── middleware.py
│   ├── urls.py
│   ├── views.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/persinfo/
│       ├── base.html
│       ├── home.html
│       ├── projects.html
│       ├── project.html
│       ├── project_detail.html
│       ├── contact.html
│       └── 429.html
└── templates/
    ├── base.html
    ├── 404.html
    ├── 500.html
    └── robots.txt
```

## Component Matrix

| File/Directory | Primary Responsibility | Main Dependencies |
| :--- | :--- | :--- |
| `mainweb/settings.py` | App configuration, security, DB cache, assets | Django, compressor, whitenoise |
| `mainweb/urls.py` | Root URLs, 404/500/429 custom error routing | Django, `persinfo.urls` |
| `persinfo/models.py` | DB Schemas (Project, Skill, ContactMessage) | Django models |
| `persinfo/middleware.py` | www-redirection and proxy-aware RateLimit enforcement | Django middleware |
| `persinfo/views.py` | Page renders, dynamic 5-project portfolio, Green API | Django, models, requests |
| `persinfo/urls.py` | Namespace routes (`persinfo`) | Django urls, `views.py` |
| `persinfo/static/` | App assets (style.css, main.js) | Static file system |
| `persinfo/templates/` | Custom HTML UI templates & Glassmorphic 429 page | Django templates |
| `Dockerfile` | Multi-process container entrypoint (auto-creates cache table) | `requirements.txt` |
| `requirements.txt` | Dependency list including `requests` and `django-ratelimit` | Python, Pip |
