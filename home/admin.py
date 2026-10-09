from django.contrib import admin

from .models import Bike, Booking, BrandContent, ChatbotMessage, ContactMessage, CustomerReview, DealerCoverageCity, DealerLocation, PageVisit


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'engine_cc', 'power_bhp', 'torque_nm', 'badge', 'is_active')
    list_filter = ('category', 'badge', 'is_active')
    search_fields = ('name', 'category', 'description')
    list_editable = ('badge', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('sort_order', 'name')
    fieldsets = (
        ('Model', {'fields': ('name', 'slug', 'category', 'model_year', 'price', 'description', 'long_description', 'design_story', 'ride_story', 'ideal_for', 'badge', 'sort_order', 'is_active')}),
        ('Engine & performance', {'fields': ('engine_cc', 'engine_configuration', 'cooling', 'fuel_system', 'power_bhp', 'torque_nm', 'transmission')}),
        ('Chassis & equipment', {'fields': ('fuel_capacity_l', 'kerb_weight_kg', 'seat_height_mm', 'front_suspension', 'rear_suspension', 'front_brake', 'rear_brake', 'safety_features')}),
        ('Rental offer', {'fields': ('is_rentable', 'rental_daily_rate', 'rental_deposit', 'rental_min_days', 'rental_max_days', 'rental_units', 'rental_terms')}),
        ('Images', {'fields': ('image', 'image_name')}),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'bike', 'booking_type', 'preferred_date', 'return_date', 'status', 'booking_date')
    list_filter = ('booking_type', 'status', 'booking_date', 'bike')
    search_fields = ('customer_name', 'email', 'phone')
    readonly_fields = ('booking_date', 'razorpay_order_id', 'razorpay_payment_id', 'amount_paise')
    date_hierarchy = 'booking_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'submitted_at'


@admin.register(BrandContent)
class BrandContentAdmin(admin.ModelAdmin):
    list_display = ('engineering_title', 'satisfaction_title')
    fieldsets = (
        ('Homepage hero', {'fields': ('home_tagline', 'home_title_line_1', 'home_title_line_2', 'home_title_line_3', 'home_description')}),
        ('Homepage commitment band', {'fields': ('home_promise_title', 'home_promise_description', 'home_cta_title')}),
        ('Heritage & founders', {'fields': ('heritage_intro', 'origin_label', 'founders_title', 'founders_names', 'founders_story', 'heritage_story')}),
        ('Commitments', {'fields': ('engineering_title', 'engineering_story', 'satisfaction_title', 'satisfaction_story')}),
    )

    def has_add_permission(self, request):
        return not BrandContent.objects.exists() and super().has_add_permission(request)


@admin.register(DealerLocation)
class DealerLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type', 'city', 'region', 'is_active')
    list_filter = ('location_type', 'is_active', 'region')
    search_fields = ('name', 'address', 'city', 'region')


@admin.register(DealerCoverageCity)
class DealerCoverageCityAdmin(admin.ModelAdmin):
    list_display = ('city', 'region', 'showroom_available', 'service_center_available', 'is_active')
    list_filter = ('showroom_available', 'service_center_available', 'is_active', 'region')
    search_fields = ('city', 'region')
    list_editable = ('showroom_available', 'service_center_available', 'is_active')


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'bike', 'rating', 'location', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published', 'bike')
    search_fields = ('customer_name', 'review', 'location')
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'user', 'visited_at')
    list_filter = ('visited_at',)
    search_fields = ('path', 'user__username', 'user__email')
    readonly_fields = ('path', 'user', 'visited_at')
    date_hierarchy = 'visited_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'role', 'user', 'conversation_id', 'preview')
    list_filter = ('role', 'created_at')
    search_fields = ('message', 'user__username', 'conversation_id')
    readonly_fields = ('user', 'conversation_id', 'role', 'message', 'created_at')
    date_hierarchy = 'created_at'

    @admin.display(description='Message')
    def preview(self, obj):
        return obj.message[:100]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.site_header = 'DAVIDPUTTRA Administration'
admin.site.site_title = 'DAVIDPUTTRA Admin'
admin.site.index_title = 'Manage your website content'
admin.site.index_template = 'admin/index.html'
