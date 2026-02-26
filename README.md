# Mailing Web App

A Django-powered mailing web application with a modern Tailwind CSS interface for sending, managing, and tracking emails efficiently.

## Setup

1. Create and activate a virtual environment.
2. Copy `.env.example` to `.env` and configure your environment variables.
3. Install dependencies.
4. Apply migrations.
5. Run the server.

```powershell
.\.venv\Scripts\Activate.ps1
cp .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `EMAIL_HOST_USER`: Your email address
- `EMAIL_HOST_PASSWORD`: Your email app password

See `.env.example` for a complete list.

## Project Layout

- `config/`: Django project settings and URLs.
- `manage.py`: Django management entry point.
