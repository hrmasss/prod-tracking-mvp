# Production Tracking using QR Code

## Project Overview

This project is a production tracking system that uses QR codes to monitor the movement of materials and bundles through a production line. It provides real-time visibility into the production process, helping to identify bottlenecks, track inventory, and improve efficiency.

### Features

-   **QR Code Scanning:** Uses device cameras to scan QR codes attached to materials and bundles.
-   **Real-Time Tracking:** Provides real-time updates on the location of materials and bundles within the production line.
-   **Production Line Management:** Allows defining and managing production lines and scanning stations.
-   **Inventory Management:** Tracks the quantity of materials and bundles in each production line.
-   **Reporting and Analytics:** Generates reports and analytics on production progress, material usage, and potential shortages.
-   **Dashboard:** Provides a visual overview of the production process, including key metrics and charts.
-   **User Authentication:** Secure user authentication and authorization.

### Scope and Goals

The scope of this project is to develop a comprehensive production tracking system that can be used by small to medium-sized manufacturing companies. The goals of the project are to:

-   Improve production efficiency by providing real-time visibility into the production process.
-   Reduce inventory losses by accurately tracking the movement of materials and bundles.
-   Identify and resolve bottlenecks in the production line.
-   Provide data-driven insights to optimize production processes.
-   Reduce manual data entry and improve data accuracy.

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
│   ├── __init__.py
│   ├── admin.py
│   ├── fields.py
│   ├── models.py
│   ├── unfold.py
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
├── users/                  # Authentication & authorization
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── migrations/
│   └── ...
├── tracker/                # Production tracking application
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── utils.py
│   ├── migrations/
│   └── ...
├── tests/                  # Test suites
│   ├── conftest.py
│   └── ...
├── logs/                   # Application logs
├── templates/              # Project-level templates
├── static/                 # Project-level static files
├── media/                  # Media files
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

6. Seed test data (optional):

```bash
python manage.py seed_dev  # Creates basic test data and superuser (admin/admin)
python manage.py seed_dev --full  # Creates more comprehensive test data
```

This command will also create a superuser with the username `admin` and password `admin`.

7. Create a superuser (if not using seed data):

```bash
python manage.py createsuperuser
```

8. Collect static files:

```bash
python manage.py collectstatic
```

9. Run the development server:

```bash
python manage.py runserver
```

The development server should now be running at `http://localhost:8000`.

10. **Running HTTPS server for phone testing (optional):**

    To test the QR scanning functionality on a phone (accessing the server via the network), you need to run the development server with HTTPS because camera permissions don't work without HTTPS or `localhost`.

    ```bash
    python manage.py runserver_plus --key-file selftest-key --cert-file selftest-cert 0.0.0.0:9000
    ```

    This will start the server on all interfaces (`0.0.0.0`) on port `9000` using a self-signed certificate. You can then access the server from your phone using the server's IP address (e.g., `https://192.168.1.100:9000`).

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

3. Run migrations and seed data:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed_dev # Creates basic test data and superuser (admin/admin)
docker-compose exec backend python manage.py seed_dev --full  # Creates more comprehensive test data
```

4. Create superuser (if not using seed data):

```bash
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
