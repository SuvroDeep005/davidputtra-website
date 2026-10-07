# DAVIDPUTTRA

A Django website for the DAVIDPUTTRA motorcycle brand, with model and performance pages, editable brand and dealer content, customer accounts, bookings, reviews, and an optional Razorpay checkout.

## Run locally

Requirements: Python 3.12 or newer.

1. Create and activate a virtual environment.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and replace `DJANGO_SECRET_KEY` with a unique local secret.
4. Apply database migrations: `python manage.py migrate`.
5. Create an admin account: `python manage.py createsuperuser`.
6. Start Django: `python manage.py runserver`.

If `DB_NAME` is not set, the project uses a local SQLite database. Set all `DB_*` variables in `.env` to use PostgreSQL instead. Local uploads and credentials are excluded from Git; the bike photos needed by the site are included in `media/bikes/`.

## Site administration

Visit `/admin/` to manage motorcycles, brand content, dealer locations, customer reviews, bookings, and contact enquiries. Model photo files are stored in `media/bikes/`.

## Razorpay

Payments are optional and disabled by default. To enable test checkout, add your Razorpay test key ID and secret to `.env` and set `RAZORPAY_BOOKING_FEE_PAISE` to the agreed fee in paise. Keep the secret key private and use test mode until checkout has been verified.

## Collaboration

Use feature branches for changes, then open a pull request for review before merging into `main`. Never commit `.env`, database files, customer uploads, or production credentials.
