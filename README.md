# BarberGeelAppointment

**BarberGeelAppointment** is an online appointment booking system for barbershops. It allows clients to schedule appointments online, receive email reminders, and pay securely through an integrated payment gateway. This project is built with Django and provides an easy-to-use interface for both customers and staff.

## Live Demo

You can try out the live demo of the project here: [BarberGeelAppointment Demo](https://barber-appointment.liara.run/)

## Features

- **Online Appointment Booking**: Clients can select a preferred date and time for various barbershop services.
- **Email Reminder System**: Sends a reminder email to the client three hours before their scheduled appointment, ensuring they remember their booking. This reminder only sends for confirmed bookings.
- **Online Payment Integration**: Secure payment processing using Zarinpal, allowing customers to pay in advance for their bookings.
- **Daily Capacity Limit**: Limits the number of bookings per day to manage workload effectively.
- **Validation System**: Prevents booking for past dates and times, ensuring all appointments are valid.

## Prerequisites

Make sure you have the following installed before running the project:

- Python 3.8 or higher
- Django 3.2 or higher
- PostgreSQL
- Additional packages: `requests`, `django-jalali`, and `django-crispy-forms`

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Mohammadparsa1384/barberGeelAppointment.git
   cd barberGeelAppointment
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:

   Create an `.env` file in the root of your project and add the following configuration settings:

   ```env
   DJANGO_SECRET_KEY=<your-secret-key>
   EMAIL_HOST_USER=<your-email>
   EMAIL_HOST_PASSWORD=<your-email-password>
   EMAIL_USE_TLS=True
   ZARINPAL_MERCAHNTID=<your-zarinpal-merchant-id>
   DJANGO_DEBUG=True
   POSTGRES_NAME=<your-database-name>
   POSTGRES_USER=<your-database-user>
   POSTGRES_PASSWORD=<your-database-password>
   ```

   Alternatively, you can use the provided `example.env` file and fill in the required values.

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for accessing the Django admin interface):

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the project**:

   Visit `http://127.0.0.1:8000/` to access the application. You can log in as an admin at `http://127.0.0.1:8000/admin`.

## Usage

Once set up, clients can book appointments by selecting a date and time within business hours (9 AM to 9 PM). They will receive an email confirmation upon booking and a reminder email three hours before the appointment. If payment is required, they can pay securely through Zarinpal.

## Project Structure

- `appointment/`: Contains the main booking functionality, including views, models, and forms.
- `templates/`: Contains HTML templates for the user interface.
- `static/`: Contains static files like CSS and JavaScript for styling and interactivity.
- `settings.py`: Configures Django settings, including database, authentication, and email settings.

## Running with PostgreSQL

If you want to use PostgreSQL instead of SQLite, update your `.env` file with your PostgreSQL credentials and modify the `DATABASES` setting in `settings.py` accordingly:

```python
from environs import Env

env = Env()
env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_NAME'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': 'localhost',  # Change this if using a remote database
        'PORT': '5432',  # Default PostgreSQL port
    }
}
```

Now, restart your server to apply the changes:

```bash
python manage.py runserver
```

