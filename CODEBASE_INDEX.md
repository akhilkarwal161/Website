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
|  |  | DB |  | File Cache |                         |  |
|  |  |    |  | (django_   |                         |  |
|  |  |    |  |  cache)    |                         |  |
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
│       └── contact.html
└── templates/
    ├── base.html
    ├── 404.html
    ├── 500.html
    └── robots.txt
```

## Component Matrix

| File/Directory | Primary Responsibility | Main Dependencies |
| :--- | :--- | :--- |
| `mainweb/settings.py` | App configuration, security, caching, assets | Django, compressor, whitenoise |
| `mainweb/urls.py` | Root URLs, 404/500 custom error routing, robots.txt | Django, `persinfo.urls` |
| `persinfo/models.py` | DB Schemas (Project, Skill, ContactMessage) | Django models |
| `persinfo/views.py` | Page renders & core application business logic | Django, models |
| `persinfo/urls.py` | Namespace routes (`persinfo`) | Django urls, `views.py` |
| `persinfo/static/` | App assets (style.css, main.js) | Static file system |
| `persinfo/templates/` | Custom HTML UI templates | Django templates |
| `Dockerfile` | Production server build (Python Alpine + Gunicorn) | `requirements.txt` |
| `requirements.txt` | PyPI third-party package manifest | Python |
