# ✍️ BlogPlatform

A full-featured **Blog Platform** built with Python & Django — featuring user authentication, rich blog post management, categories, comments, likes, search, and a stunning dark-mode UI.

🚀 **Live Demo:** [https://chakrastra.pythonanywhere.com/](https://chakrastra.pythonanywhere.com/)

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat-square&logo=django)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Auth** | Register, Login, Logout with flash messages |
| 📝 **Blog Posts** | Full CRUD — Create, Read, Update, Delete |
| 📂 **Categories** | Colour-coded categories with filtering pages |
| 🔍 **Search** | Search by title, body, category, or author |
| ❤️ **Likes** | AJAX-powered like/unlike with live count update |
| 💬 **Comments** | Post & delete comments on any article |
| 📊 **Dashboard** | Author stats (posts, likes, comments) + posts table |
| 📄 **Pagination** | 6 posts per page with next/prev controls |
| ⚙️ **Admin Panel** | Full Django admin for all models |
| 📱 **Responsive** | Works on mobile and desktop |

---

## 🖥️ Screenshots

### Homepage
Dark-themed hero section with search, category filters, and post cards.

### Dashboard
Stat cards showing total posts, likes, comments, and a full posts management table.

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Chakrastra/BlogPlatform.git
cd BlogPlatform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file
cp .env.example .env

# 4. Run migrations
python manage.py migrate

# 5. (Optional) Seed with sample data
python seed_data.py

# 6. Start the dev server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 👤 Demo Accounts (after running seed_data.py)

| Username | Password   | Role |
|----------|------------|------|
| `admin`  | `admin123` | Superuser |
| `alice`  | `Alice123!` | Author |
| `bob`    | `Bob12345!` | Author |
| `carol`  | `Carol123!` | Author |

Admin panel → **http://127.0.0.1:8000/admin/**

---

## 🗂️ Project Structure

```
BlogPlatform/
├── blog/                   # Main Django app
│   ├── models.py           # Post, Category, Comment, Like
│   ├── views.py            # All views + AJAX like toggle
│   ├── forms.py            # PostForm, CommentForm, RegisterForm
│   ├── urls.py
│   └── admin.py
├── blogplatform/           # Project config
│   ├── settings.py         # Production-ready settings
│   └── urls.py
├── templates/              # HTML templates (dark UI)
│   ├── base.html
│   ├── blog/
│   └── registration/
├── static/css/style.css    # Dark glassmorphism theme
├── requirements.txt
├── Procfile                # Gunicorn for deployment
├── railway.toml            # Railway deployment config
├── seed_data.py            # Populate demo data
└── .env.example            # Environment variables template
```

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Django 5.0
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Static Files:** WhiteNoise
- **Web Server:** Gunicorn
- **Frontend:** Vanilla HTML/CSS (dark glassmorphism theme)
- **Fonts:** Google Fonts (Inter + Playfair Display)

---

## 📄 License

This project is licensed under the **MIT License**.
