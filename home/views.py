import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import Bike, Booking, BrandContent, ContactMessage, CustomerReview, DealerCoverageCity, DealerLocation


def _brand_content():
    return BrandContent.objects.first() or BrandContent()


def home1(request):
    bikes = Bike.objects.filter(is_active=True)
    reviews = CustomerReview.objects.filter(is_published=True).select_related('bike')[:6]
    return render(request, 'Home1.html', {'bikes': bikes, 'reviews': reviews})


def Models1_page(request):
    bikes = Bike.objects.filter(is_active=True)
    return render(request, 'Models1.html', {'bikes': bikes})


def bike_detail(request, slug):
    if slug == 'davidputtra-xc':
        return redirect('BikeDetail', slug='davidputtra-v4s', permanent=True)
    bike = get_object_or_404(Bike, slug=slug, is_active=True)
    reviews = CustomerReview.objects.filter(is_published=True).filter(Q(bike=bike) | Q(bike__isnull=True))[:4]
    return render(request, 'BikeDetail.html', {'bike': bike, 'reviews': reviews})


def performance1_page(request):
    bikes = Bike.objects.filter(is_active=True)
    return render(request, 'Performance1.html', {'bikes': bikes})


def dealers1_page(request):
    locations = DealerLocation.objects.filter(is_active=True)
    coverage_cities = list(DealerCoverageCity.objects.filter(is_active=True))
    for city in coverage_cities:
        if city.latitude is not None and city.longitude is not None:
            longitude, latitude = float(city.longitude), float(city.latitude)
            city.map_x = max(1, min(99, (longitude - 66.5) / 33 * 100))
            city.map_y = max(1, min(99, (37.5 - latitude) / 32 * 100))
        else:
            city.map_x = city.map_y = 50
    locations_with_map = []
    for location in locations:
        location.map_embed_url = bool(location.latitude is not None and location.longitude is not None)
        locations_with_map.append(location)
    return render(request, 'Dealers1.html', {
        'locations': locations_with_map,
        'coverage_cities': coverage_cities,
    })


def contact1_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('Contact')
        messages.error(request, 'Please complete your name, email and message.')
    return render(request, 'Contact1.html')


def heritage1_page(request):
    return render(request, 'Heritage1.html', {'brand': _brand_content()})


def _razorpay_request(path, payload=None, method='POST'):
    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET
    credentials = base64.b64encode(f'{key_id}:{key_secret}'.encode()).decode()
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        f'https://api.razorpay.com/v1/{path}', data=body, method=method,
        headers={'Authorization': f'Basic {credentials}', 'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ValueError('Razorpay could not be reached. Please try again later.') from exc


def _rental_dates_available(bike, start_date, return_date):
    recent_pending = timezone.now() - timedelta(minutes=15)
    overlapping = Booking.objects.filter(
        bike=bike,
        booking_type='rental',
        preferred_date__lt=return_date,
        return_date__gt=start_date,
    ).filter(
        Q(status='confirmed') | Q(status='pending_payment', booking_date__gte=recent_pending)
    )
    return overlapping.count() < bike.rental_units


def book_now(request):
    bikes = Bike.objects.filter(is_active=True)
    rentable_bikes = bikes.filter(
        is_rentable=True,
        rental_daily_rate__gt=0,
        rental_deposit__isnull=False,
        rental_units__gt=0,
    ).exclude(rental_terms='')
    booking_type = request.POST.get('booking_type', request.GET.get('type', 'test_ride'))
    if booking_type not in ('test_ride', 'rental'):
        booking_type = 'test_ride'
    booking_context = {
        'bikes': bikes,
        'rentable_bikes': rentable_bikes,
        'rental_catalog': bikes,
        'booking_type': booking_type,
        'fee_paise': settings.RAZORPAY_BOOKING_FEE_PAISE,
        'fee_display': f'{settings.RAZORPAY_BOOKING_FEE_PAISE / 100:.2f}',
        'fee_currency': settings.RAZORPAY_CURRENCY,
        'razorpay_configured': bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET),
        'today': timezone.localdate(),
        'selected_bike': request.POST.get('bike', request.GET.get('bike', '')),
        'initial_name': request.POST.get('name', request.user.get_full_name() if request.user.is_authenticated else ''),
        'initial_email': request.POST.get('email', request.user.email if request.user.is_authenticated else ''),
        'initial_phone': request.POST.get('phone', ''),
        'initial_location': request.POST.get('location', ''),
    }
    if request.method == 'POST':
        bike_queryset = bikes
        if booking_type == 'rental':
            bike_queryset = rentable_bikes
        bike = get_object_or_404(bike_queryset, pk=request.POST.get('bike'))
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        location = request.POST.get('location', '').strip()
        preferred_date = parse_date(request.POST.get('rental_start', '') if booking_type == 'rental' else request.POST.get('date', ''))
        return_date = parse_date(request.POST.get('rental_return', '')) if booking_type == 'rental' else None
        if not (name and email and phone):
            messages.error(request, 'Please enter your name, email and phone number.')
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
        if len(name) > 100 or len(email) > 254 or len(phone) > 20:
            messages.error(request, 'Please check the length of your contact details and try again.')
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
        if len(location) > 150:
            messages.error(request, 'Please shorten the city or pickup location and try again.')
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})

        rental_days = 0
        rental_rate = None
        rental_deposit = None
        if booking_type == 'rental':
            if not preferred_date or not return_date:
                messages.error(request, 'Choose both your rental start and return dates.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            if preferred_date < timezone.localdate() or return_date <= preferred_date:
                messages.error(request, 'Choose a future start date and a return date after the start date.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            rental_days = (return_date - preferred_date).days
            if rental_days < bike.rental_min_days or (bike.rental_max_days and rental_days > bike.rental_max_days):
                maximum = f' and no more than {bike.rental_max_days}' if bike.rental_max_days else ''
                messages.error(request, f'This model has a minimum rental period of {bike.rental_min_days} days{maximum}.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            if not location:
                messages.error(request, 'Enter the city where you would like to collect the motorcycle.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            if not request.POST.get('agree_rental_terms'):
                messages.error(request, 'Please review and accept the rental terms before continuing.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            if not _rental_dates_available(bike, preferred_date, return_date):
                messages.error(request, 'This model is not available for the selected dates. Please choose other dates or contact us.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            rental_rate = bike.rental_daily_rate
            rental_deposit = bike.rental_deposit or Decimal('0.00')
            amount = int(((rental_rate * rental_days + rental_deposit) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        else:
            if preferred_date and preferred_date < timezone.localdate():
                messages.error(request, 'Please choose today or a future date.')
                return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
            amount = settings.RAZORPAY_BOOKING_FEE_PAISE

        if amount > 0 and not (settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET):
            messages.error(request, 'Online payment is not configured yet. Please contact us to arrange your ride.')
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})

        booking = Booking.objects.create(
            bike=bike, customer=request.user if request.user.is_authenticated else None,
            booking_type=booking_type,
            customer_name=name, email=email, phone=phone, preferred_date=preferred_date,
            return_date=return_date, rental_days=rental_days,
            rental_daily_rate=rental_rate, rental_deposit=rental_deposit,
            amount_paise=amount, location=location,
            status='requested' if amount <= 0 else 'pending_payment',
        )
        if amount <= 0:
            messages.success(request, 'Your test-ride request is in. Our team will be in touch.')
            return redirect('BookNow')
        try:
            order = _razorpay_request('orders', {
                'amount': amount,
                'currency': settings.RAZORPAY_CURRENCY,
                'receipt': f'booking-{booking.pk}',
                'notes': {'booking_id': str(booking.pk), 'bike': bike.name, 'booking_type': booking_type},
            })
            booking.razorpay_order_id = order['id']
            booking.save(update_fields=['razorpay_order_id'])
            return render(request, 'Payment.html', {
                'booking': booking, 'order_id': order['id'], 'amount': amount,
                'total_display': f'{amount / 100:.2f}',
                'key_id': settings.RAZORPAY_KEY_ID,
                'currency': settings.RAZORPAY_CURRENCY,
                'fee_currency': settings.RAZORPAY_CURRENCY,
                'success_url': reverse('PaymentSuccess', args=[booking.pk]),
            })
        except (KeyError, ValueError) as exc:
            booking.status = 'payment_failed'
            booking.save(update_fields=['status'])
            messages.error(request, str(exc))
            return render(request, 'BookNow.html', {**booking_context, 'selected_bike': bike.pk})
    return render(request, 'BookNow.html', booking_context)


def payment_success(request, booking_id):
    if request.method != 'POST':
        return redirect('BookNow')
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.customer_id and booking.customer_id != getattr(request.user, 'pk', None):
        return redirect('BookNow')
    payment_id = request.POST.get('razorpay_payment_id', '')
    order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')
    message = f'{order_id}|{payment_id}'.encode()
    expected = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), message, hashlib.sha256).hexdigest()
    if order_id != booking.razorpay_order_id or not hmac.compare_digest(expected, signature):
        messages.error(request, 'We could not verify that payment. Please contact our team.')
        return redirect('BookNow')
    try:
        payment = _razorpay_request(f'payments/{payment_id}', method='GET')
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('BookNow')
    expected_amount = booking.amount_paise or settings.RAZORPAY_BOOKING_FEE_PAISE
    if (payment.get('order_id') != order_id or payment.get('status') != 'captured'
            or payment.get('amount') != expected_amount
            or payment.get('currency') != settings.RAZORPAY_CURRENCY):
        messages.error(request, 'Payment has not been captured yet. Please contact our team if you were charged.')
        return redirect('BookNow')
    booking.status = 'confirmed'
    booking.razorpay_payment_id = payment_id
    booking.save(update_fields=['status', 'razorpay_payment_id'])
    return render(request, 'PaymentSuccess.html', {'booking': booking})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Account')
    else:
        form = UserCreationForm()
    return render(request, 'Register.html', {'form': form})


@login_required
def account(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('bike')
    return render(request, 'Account.html', {'bookings': bookings})


def logout_customer(request):
    if request.method == 'POST':
        logout(request)
    return redirect('Home')
