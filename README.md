# Mailing Web App

A production-ready Django web application with MongoDB and Tailwind CSS for sending, managing, and tracking emails efficiently.

## Features

- 🔐 **User Authentication** - Register, login, and logout functionality
- 📧 **Send Emails** - Compose and send emails via SMTP
- 📊 **Email History** - Track all sent emails with timestamps
- 🎨 **Modern UI** - Responsive design with Tailwind CSS
- 🗄️ **MongoDB Database** - NoSQL database using djongo
- ⚡ **Production Ready** - Environment-based configuration

## Tech Stack

- **Backend**: Django 6.0.1
- **Database**: MongoDB (via djongo & pymongo)
- **Frontend**: Tailwind CSS 3.4+
- **Email**: SMTP (Gmail)
- **Environment**: python-decouple

## Prerequisites

- Python 3.10+
- Node.js 16+ (for Tailwind CSS)
- MongoDB (local or MongoDB Atlas)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rishabhtcodes/Mailing-Web-App.git
cd Mailing-Web-App
```

### 2. Create Virtual Environment

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```powershell
cp .env.example .env
```

Update the following in `.env`:
- `SECRET_KEY`: Generate a new secret key for production
- `DEBUG`: Set to `False` in production
- `MONGO_URI`: Your MongoDB connection string
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Gmail App Password ([How to create](https://support.google.com/accounts/answer/185833))

### 5. Setup MongoDB

**Option A: Local MongoDB**
```bash
# Ensure MongoDB is running on localhost:27017
# Connection string: mongodb://localhost:27017/
```

**Option B: MongoDB Atlas (Cloud)**
```bash
# Create a free cluster at https://www.mongodb.com/cloud/atlas
# Get your connection string and add to MONGO_URI in .env
# Example: mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 6. Install Node Dependencies & Build Tailwind CSS

```bash
npm install
npm run tailwind:build
```

For development with auto-rebuild:
```bash
npm run dev
```

### 7. Run Migrations

```bash
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
Mailing_Web_App/
├── apps/
│   ├── users/              # Authentication app
│   │   ├── views.py        # Login, register, dashboard
│   │   └── urls.py
│   └── mailapp/            # Email system app
│       ├── models.py       # EmailHistory model
│       ├── views.py        # Send email, history
│       └── urls.py
├── config/                 # Main project settings
│   ├── settings.py         # Django configuration
│   └── urls.py             # URL routing
├── templates/              # HTML templates
│   ├── base.html           # Base template with navbar
│   ├── index.html          # Homepage
│   ├── users/              # User templates
│   └── mailapp/            # Email templates
├── static/
│   ├── src/
│   │   └── input.css       # Tailwind source
│   └── css/
│       └── output.css      # Compiled CSS
├── .env                    # Environment variables (gitignored)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies
├── tailwind.config.js      # Tailwind configuration
└── manage.py               # Django CLI
```

## Usage

### Register/Login
1. Navigate to `/users/register/` to create an account
2. Login at `/users/login/`
3. Access dashboard at `/users/dashboard/`

### Send Email
1. Go to `/mail/send/`
2. Fill in recipient, subject, and message
3. Click "Send Email"
4. Email is sent via SMTP and stored in MongoDB

### View History
1. Navigate to `/mail/history/`
2. See all emails you've sent with timestamps

## Available Scripts

### Django
- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py makemigrations` - Create new migrations

### Tailwind CSS
- `npm run dev` - Watch mode (auto-rebuild on changes)
- `npm run tailwind:build` - Build for production
- `npm run tailwind:watch` - Watch mode alias

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `True` or `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `MONGO_URI` | MongoDB connection | `mongodb://localhost:27017/` |
| `EMAIL_BACKEND` | Email backend | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS | `True` |
| `EMAIL_HOST_USER` | Your email | `your_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App password | `your_app_password` |

## Gmail Setup

To use Gmail SMTP:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated 16-character password in `EMAIL_HOST_PASSWORD`

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use production-grade MongoDB (MongoDB Atlas recommended)
4. Run `npm run tailwind:build` for optimized CSS
5. Collect static files: `python manage.py collectstatic`
6. Use a production WSGI server (gunicorn, uvicorn)

## License

MIT
