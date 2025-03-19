# Production Tracking using QR Code

## Project Overview

...

### Features

...

### Scope and Goals

...

## System Components

```
┌─────────────────┐     ┌─────────────────┐
│  MVC Framework  │     │    Database     │
│     (Django)    │────▶│  (PostgreSQL)   │
└─────────────────┘     └─────────────────┘
        │
        │
┌───────▼───────┐
│Background Jobs│
│    (Celery)   │
└───────────────┘
```

### Technology Stack

-   Python 3.12+
-   Django 5.1+
-   PostgreSQL 16+
-   Poetry (Dependency Management)
-   Docker (Containerization)

### Project Structure

```
ocr-backend/
├── core/                   # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── ...
├── common/                 # Shared components
│   ├── views.py
│   ├── models.py
│   ├── fields.py
│   └── ...
├── users/                  # Authentication & authorization
│   ├── viws.py
│   ├── backends.py
│   ├── models.py
│   └── ...
├── tests/                  # Test suites
│   ├── conftest.py
│   └── ...
├── logs/                   # Application logs
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Getting Started

### Prerequisites

-   Python 3.12+
-   PostgreSQL 16+
-   Poetry
-   Docker (optional)

### Development Setup Using Poetry

1. Clone the repository:

```bash
git clone https://github.com/hapltech/humanaapparels.git
cd humanaapparels
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Install dependencies using Poetry:

```bash
poetry install
```

4. Activate the virtual environment:

```bash
poetry shell
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Collect static files:

```bash
python manage.py collectstatic
```

8. Run the development server:

```bash
python manage.py runserver
```

### Development Setup Using Docker

1. Clone and setup environment:

```bash
git clone https://github.com/hapltech/humanaapparels.git
cd humanaapparels
cp .env.example .env
```

2. Build and start containers:

```bash
docker-compose up --build
```

3. Run migrations and create superuser:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Environment Variables

Required environment variables in `.env`:

```
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```
