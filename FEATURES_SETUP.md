# DAVIDPUTTRA website content and customer features

## Apply the database changes

Back up the database, then run the new migration from the Django project folder:

```powershell
python manage.py migrate
```

The migration adds three starter motorcycle records using the specifications already shown on the website, plus editable brand-story content. It does not create sample locations or customer reviews.

## Edit website content

Sign in to `/admin/` with a staff account.

- **Bikes:** Edit descriptions, longer model copy, specifications, images, display order and active status. Home, Models, Performance and individual model pages use the same records.
- **Brand content:** Edit the heritage story and the engineering and customer-care commitments.
- **Dealer locations:** Add one record per showroom or service center. Enter the full address and latitude/longitude to show its map pin. The map uses OpenStreetMap.
- **Customer reviews:** Add real customer feedback, then enable **Published** to show it publicly. New reviews are private by default.
- **Bookings and messages:** Review customer requests and contact enquiries in the admin.

Customer registration and sign-in are available from the main navigation. Test-ride and rental booking pages require sign-in. A signed-in customer can see only their own requests under **My Account**. Admin users can review all bookings, contact messages, chatbot conversations, page traffic and Django admin change history. Customer records and analytics are private to staff accounts.

## Configure Razorpay

The checkout integration is inactive until a positive booking fee and Razorpay API keys are configured. Put the values in the project's existing local `.env` file; use the test keys first:

```text
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_BOOKING_FEE_PAISE=100000
RAZORPAY_CURRENCY=INR
```

`100000` is ₹1,000.00. Choose the actual reservation amount before enabling payment. Use Razorpay test mode and complete a test transaction before replacing test keys with live keys. Configure automatic capture in the Razorpay Dashboard; the site marks a paid booking confirmed only after Razorpay reports the payment as captured. Keep the key secret on the server and never put it in a template or JavaScript.

See Razorpay's [Python integration guide](https://razorpay.com/docs/server-integration/python/test-app/) for account, key and test-mode setup.
