# DAVIDPUTTRA Project Context

## Project location
- Django project root: C:\Django project\Hello
- Django project package: Hello
- Main application: home
- Templates: Templates/
- Source static assets: static/
- Collected static assets: staticfiles/
- Uploaded media: media/

## Current client page
- At the last observed browser state (2026-10-09), the site was open at http://localhost/Contact/.
- The client is currently reviewing the Contact page.

## Application structure
- Hello/urls.py is the main URL router. / and /Home/ both display the home page.
- Templates/Base4.html is the shared layout and navigation. It includes the Home button and chatbot widget.
- home/views.py loads page data, handles booking authentication, and implements the FAQ chatbot endpoint.
- home/models.py contains bike, booking, brand, dealer, customer review, page visit, and chatbot message records.
- Django Admin manages bikes, brand story and homepage content, reviews, dealer coverage and locations, bookings, contact messages, chatbot conversations, and page traffic.
- New customers are sent to Login before booking. Login links to registration, and registration returns them to the intended booking page. Payment confirmation is restricted to the booking's customer.
- The chatbot is a rule-based FAQ helper, not connected to an external AI service. It uses current site data and stores customer and assistant messages for staff review.
- The Admin dashboard shows user, booking, message and visit totals, a seven-day traffic chart, popular pages, booking states, and recent Django admin changes. Customer records are staff-only.

## Local run and static-file notes
- Install dependencies with python -m pip install -r requirements.txt.
- Apply schema changes with python manage.py migrate.
- Development server: python manage.py runserver.
- Waitress: waitress-serve --listen=127.0.0.1:8000 Hello.wsgi:application.
- The observed local setup had Nginx on port 80 and Waitress on port 8000. Browser address localhost uses Nginx; localhost:8000 reaches Waitress.
- Nginx serves collected assets from staticfiles/. After changing CSS, JavaScript, or images, run python manage.py collectstatic --noinput and hard-refresh the browser.
- staticfiles/ is generated, but currently needed by the local Nginx setup. Do not delete it without recollecting static assets.
- .env contains local credentials and is ignored by Git. Never print, commit, or copy its contents into notes.
- Razorpay is integrated in code but was not configured in the observed environment; a test/live key ID, secret, and agreed booking fee are needed to enable checkout.

## Recent project state
- Migration home/migrations/0018_brandcontent_home_cta_title_and_more.py was generated and applied to the configured local database.
- Waitress was added to requirements.txt.
- At the last project review, website code edits were still uncommitted. Check git status before committing or synchronizing with the collaborator.
- Generated Python __pycache__ folders were removed; Python recreates them automatically.

## Collaboration notes
- Preserve the existing local .env, customer database, media, motorcycle photos, and VS Code launch configuration.
- Before removing other files, check whether Django, Nginx, the admin site, or the database depends on them.


## Latest navigation and responsive pass (2026-10-09)
- Shared navigation in `Templates/Base4.html` includes the Home page, a clickable wordmark, active-page `aria-current` state, and a mobile menu that closes after selecting a link or pressing Escape.
- Footer navigation now points to the real site routes and has clickable telephone and email links.
- Each public/customer page has its own title and meta description. `static/favicon.svg` is the brand favicon.
- `Templates/404.html` is the branded not-found page. The final URL pattern routes unmatched paths to it during local development as well as production.
- Contact form Subject is persisted in `ContactMessage.subject` and appears in Django Admin. Migration `home/migrations/0019_contactmessage_subject.py` has been applied. Invalid submissions keep the entered values and show an error; valid submissions show a success notice.
- Login, registration and booking inputs include useful placeholder/autofill hints. Payment checkout now displays a useful message if Razorpay Checkout fails to load.
- `static/style6.css` has global overflow safeguards, narrow-screen layout refinements, accessible focus styles, and reduced-motion/mobile-background handling. Its cache version in `Base4.html` is `20261009-3`.
- After edits, `collectstatic` was run and the local Waitress process was restarted. Django system check and migration consistency check passed; main internal page links and a sample 404 were smoke-checked.
