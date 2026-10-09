from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


class Bike(models.Model):
    BADGE_CHOICES = [
        ('bestseller', 'Bestseller'),
        ('new', 'New'),
        ('flagship', 'Flagship'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, db_index=False, blank=True)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    design_story = models.TextField(blank=True, help_text='Design details shown on the model page.')
    ride_story = models.TextField(blank=True, help_text='Describe the riding character without adding unverified specifications.')
    ideal_for = models.CharField(max_length=220, blank=True, help_text='A short rider profile, such as city-to-weekend riding.')
    model_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Model year', help_text='Enter the model/manufacturing year when confirmed.')
    engine_cc = models.PositiveIntegerField(default=0, verbose_name='Engine (cc)')
    power_bhp = models.PositiveIntegerField(default=0, verbose_name='Power (BHP)')
    torque_nm = models.PositiveIntegerField(default=0, verbose_name='Torque (Nm)')
    engine_configuration = models.CharField(max_length=80, blank=True, help_text='For example, parallel twin or V4.')
    cooling = models.CharField(max_length=80, blank=True, help_text='For example, liquid-cooled.')
    fuel_system = models.CharField(max_length=100, blank=True)
    transmission = models.CharField(max_length=100, blank=True)
    fuel_capacity_l = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Fuel capacity (L)')
    kerb_weight_kg = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kerb weight (kg)')
    seat_height_mm = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Seat height (mm)')
    front_suspension = models.CharField(max_length=140, blank=True)
    rear_suspension = models.CharField(max_length=140, blank=True)
    front_brake = models.CharField(max_length=140, blank=True)
    rear_brake = models.CharField(max_length=140, blank=True)
    safety_features = models.CharField(max_length=240, blank=True, help_text='List only confirmed rider-assistance and safety equipment.')
    is_rentable = models.BooleanField(default=False, help_text='Show the rental option only after rates, availability and terms are configured.')
    rental_daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Rental rate per day')
    rental_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Rental security deposit')
    rental_min_days = models.PositiveSmallIntegerField(default=1, verbose_name='Minimum rental days')
    rental_max_days = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Maximum rental days')
    rental_units = models.PositiveSmallIntegerField(default=1, verbose_name='Rental fleet quantity', help_text='Number of this model available to rent at the selected location.')
    rental_terms = models.TextField(blank=True, help_text='Rental terms displayed before checkout.')
    image = models.ImageField(upload_to='bikes/', blank=True)
    image_name = models.CharField(max_length=120, blank=True, help_text='Optional existing file name in the static folder.')
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('sort_order', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [('test_ride', 'Test ride'), ('rental', 'Rental')]
    STATUS_CHOICES = [
        ('requested', 'Request received'),
        ('pending_payment', 'Pending payment'),
        ('confirmed', 'Confirmed'),
        ('payment_failed', 'Payment failed'),
    ]
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default='test_ride')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True, help_text='Rental return date; end date is exclusive for duration calculation.')
    rental_days = models.PositiveSmallIntegerField(default=0)
    rental_daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Rate snapshot when this rental was booked.')
    rental_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Deposit snapshot when this rental was booked.')
    amount_paise = models.PositiveBigIntegerField(default=0, help_text='Amount charged through Razorpay in currency subunits.')
    location = models.CharField(max_length=150, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.customer_name} - {self.bike.name}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.submitted_at:%Y-%m-%d}'


class BrandContent(models.Model):
    heritage_intro = models.CharField(max_length=240, default='An Indian point of view, a clear sense of purpose, and a road still unfolding.')
    origin_label = models.CharField(max_length=120, default='WEST BENGAL, INDIA')
    founders_title = models.CharField(max_length=180, default='Three friends. One shared passion for riding.')
    founders_names = models.CharField(max_length=180, default='Suvro, Roumo & Pramit')
    founders_story = models.TextField(default='DAVIDPUTTRA is a West Bengal-based motorcycle brand founded by three friends: Suvro, Roumo and Pramit. All three are passionate riders. Their shared love of motorcycles inspired them to create a brand shaped by an Indian point of view and a close connection to riders.')
    heritage_story = models.TextField(default='Every road asks something different of a motorcycle. From the close rhythm of city traffic to the open stretch beyond familiar places, riders look for confidence, character and a machine that feels their own.\n\nDAVIDPUTTRA is shaped around that idea. Our Indian perspective informs how we think about design and the riding experience: expressive machines, purposeful performance and a closer connection to the people who ride them. We keep looking forward while staying grounded in the spirit of the road.')
    engineering_title = models.CharField(max_length=120, default='Precision in every detail.')
    engineering_story = models.TextField(default='Precision engineering starts with a clear purpose. We consider how a motorcycle looks, feels and responds, then pay attention to the details that bring the whole experience together—from its stance and riding position to its power and everyday usability. Our aim is to balance expressive design with confidence-inspiring performance, and to share specifications clearly so riders can choose with confidence.')
    satisfaction_title = models.CharField(max_length=120, default='Riders come first.')
    satisfaction_story = models.TextField(default='Customer care should feel as personal as the ride. We want it to be straightforward to explore the lineup, speak with our team, book a test ride and find service support. Clear information, attentive follow-up and a willingness to listen are the foundations of a better relationship with every rider.')
    home_tagline = models.CharField(max_length=120, default='DIL SE INDIAN')
    home_title_line_1 = models.CharField(max_length=80, default='BUILT FOR')
    home_title_line_2 = models.CharField(max_length=80, default='LEGENDS')
    home_title_line_3 = models.CharField(max_length=80, default='ONLY.')
    home_description = models.TextField(default='Motorcycles for riders who demand character, confident performance and the freedom to take the longer road. Designed with Indian spirit. Made for every journey ahead.')
    home_promise_title = models.CharField(max_length=180, default='PRECISION ENGINEERING. CARE THAT GOES FURTHER.')
    home_promise_description = models.TextField(default='Thoughtful design and responsive support are part of the ride. Meet the people and principles behind DAVIDPUTTRA.')
    home_cta_title = models.CharField(max_length=120, default='FEEL THE DIFFERENCE.')

    def __str__(self):
        return 'Website brand story'


class DealerLocation(models.Model):
    LOCATION_CHOICES = [('showroom', 'Showroom'), ('service', 'Service center')]
    name = models.CharField(max_length=120)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    address = models.CharField(max_length=240)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, verbose_name='State / region')
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Required to place this location on the map.')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Required to place this location on the map.')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('city', 'name')

    def __str__(self):
        return f'{self.name} — {self.city}'


class DealerCoverageCity(models.Model):
    city = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, blank=True, verbose_name='State / territory')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='City-centre map pin; use a branch pin in Showroom & Service Locations for exact directions.')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    showroom_available = models.BooleanField(default=True)
    service_center_available = models.BooleanField(default=True)
    availability_note = models.CharField(max_length=240, blank=True, help_text='Optional note shown beside this city.')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('city',)
        verbose_name = 'City coverage'
        verbose_name_plural = 'City coverage'

    def __str__(self):
        return f'{self.city}, {self.region}' if self.region else self.city


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100)
    bike = models.ForeignKey(Bike, null=True, blank=True, on_delete=models.SET_NULL)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.customer_name} — {self.rating}/5'


class PageVisit(models.Model):
    path = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    visited_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-visited_at',)
        verbose_name = 'Page visit'
        verbose_name_plural = 'Page visits'

    def __str__(self):
        return f'{self.path} — {self.visited_at:%Y-%m-%d %H:%M}'


class ChatbotMessage(models.Model):
    ROLE_CHOICES = [('customer', 'Customer'), ('assistant', 'Assistant')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    conversation_id = models.CharField(max_length=64, db_index=True)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Chatbot message'
        verbose_name_plural = 'Chatbot messages'

    def __str__(self):
        return f'{self.get_role_display()} — {self.created_at:%Y-%m-%d %H:%M}'
