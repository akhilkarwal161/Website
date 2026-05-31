# Akhil Karwal - Personal Portfolio

A results-oriented and passionate personal portfolio website built with Python, Django, and containerized with Docker. This application is optimized for performance, SEO, and real-time user engagement.

## 🚀 Key Features

- **Instantaneous Page Transitions**: Implements a dual-layer preloading strategy using the **Speculation Rules API** (for Chromium) and **Google Quicklink** (via IntersectionObserver) to pre-render/prefetch pages as soon as links become visible.
- **WhatsApp Notification Integration**: Real-time alerts for contact form submissions delivered directly to the owner via **Green API**.
- **Premium UI/UX**: Modern, responsive design featuring a custom dribbble-style animated theme toggler (Dark/Light mode), premium project cards with hover depth, and a streamlined grid layout.
- **Production Asset Pipeline**: Integrated `django-compressor` and `WhiteNoise` for efficient minification and delivery of static assets.
- **Search Engine Optimized**: Fully configured SEO meta tags, canonical URLs, JSON-LD Schema.org markup, and GA4 (gtag.js) analytics integration.
- **Robust Security**: Includes honeypot field protection against spam bots and secure environment variable management.

## 🛠️ Tech Stack

- **Framework**: [Django 5.2.4](https://www.djangoproject.com/)
- **API Communication**: [Requests](https://requests.readthedocs.io/)
- **Server**: [Gunicorn](https://gunicorn.org/) (Multi-threaded configuration)
- **Containerization**: [Docker](https://www.docker.com/) (Alpine-based for small footprint)
- **Deployment**: [Google Cloud Run](https://cloud.google.com/run)
- **Frontend**: Vanilla CSS (Modern CSS variables, Flexbox, Grid) & Vanilla JavaScript

## 📁 Repository Structure

```
F:\REpo\Website
├── mainweb/            # Root Django configuration (settings, urls, wsgi)
├── persinfo/           # Primary application logic (models, views, templates)
│   ├── static/         # Frontend assets (CSS/JS)
│   └── templates/      # Custom HTML components
├── templates/          # Root layout and error pages (404/500)
├── Dockerfile          # Production container build instructions
├── requirements.txt    # Python package dependencies
└── CODEBASE_INDEX.md   # Detailed architectural map
```

## ⚙️ Installation & Local Setup

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized run)

### Standard Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/akhilkarwal161/Website.git
   cd Website
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

### Docker Setup
```bash
docker build -t website-portfolio .
docker run -p 8080:8080 website-portfolio
```

## ☁️ Deployment (Google Cloud Run)

The application is built to run on Cloud Run. Ensure the following environment variables are set in your service configuration:

- `DJANGO_DEBUG`: `False`
- `SECRET_KEY`: Your Django secret key
- `GREEN_API_ID`: Your Green API instance ID
- `GREEN_API_TOKEN`: Your Green API token
- `TARGET_PHONE`: WhatsApp number for notifications (e.g., `919310433121`)

## 📄 Documentation

For more detailed technical insights, refer to:
- [WHAT_HAVE_WE_ACHIEVED.md](./WHAT_HAVE_WE_ACHIEVED.md): Progress ledger and recent updates.
- [CURRENT_CONTEXT.md](./CURRENT_CONTEXT.md): Active development goals and blockers.
- [CODEBASE_INDEX.md](./CODEBASE_INDEX.md): Component-level breakdown.

## 🤝 Contact

**Akhil Karwal**  
[GitHub](https://github.com/akhilkarwal161) | [LinkedIn](https://www.linkedin.com/in/akhil-karwal-ba5114235/) | [Facebook](https://www.facebook.com/akhilkarwal161/)
