from datetime import timedelta

from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from .models import Booking, ChatbotMessage, ContactMessage, PageVisit


def admin_dashboard(request):
    if request.path.rstrip('/') != '/admin' or not request.user.is_staff:
        return {}
    today = timezone.localdate()
    first_day = today - timedelta(days=6)
    traffic = []
    for offset in range(7):
        day = first_day + timedelta(days=offset)
        visits = PageVisit.objects.filter(visited_at__date=day).count()
        traffic.append({'label': day.strftime('%a'), 'date': day, 'visits': visits})
    maximum = max((item['visits'] for item in traffic), default=0)
    for item in traffic:
        item['width'] = round(item['visits'] / maximum * 100) if maximum else 0
    thirty_days_ago = timezone.now() - timedelta(days=30)
    statuses = Booking.objects.values('status').annotate(total=Count('id')).order_by('status')
    return {
        'dashboard_users': get_user_model().objects.count(),
        'dashboard_bookings': Booking.objects.count(),
        'dashboard_messages': ContactMessage.objects.count(),
        'dashboard_chat_messages': ChatbotMessage.objects.filter(role='customer').count(),
        'dashboard_visits': PageVisit.objects.filter(visited_at__gte=thirty_days_ago).count(),
        'dashboard_traffic': traffic,
        'dashboard_top_pages': PageVisit.objects.filter(
            visited_at__gte=thirty_days_ago
        ).values('path').annotate(total=Count('id')).order_by('-total')[:6],
        'dashboard_booking_statuses': statuses,
        'dashboard_recent_logs': LogEntry.objects.select_related(
            'user', 'content_type'
        ).order_by('-action_time')[:8],
    }
