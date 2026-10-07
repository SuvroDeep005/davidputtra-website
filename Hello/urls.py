from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home1, name='Home'),
    path('Models/', views.Models1_page, name='Models'),
    path('Models/<slug:slug>/', views.bike_detail, name='BikeDetail'),
    path('Performance/', views.performance1_page, name='Performance'),
    path('Heritage/', views.heritage1_page, name='Heritage'),
    path('Dealers/', views.dealers1_page, name='Dealers'),
    path('Contact/', views.contact1_page, name='Contact'),
    path('Book-Now/', views.book_now, name='BookNow'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='PaymentSuccess'),
    path('account/login/', LoginView.as_view(template_name='Login.html', redirect_authenticated_user=True), name='Login'),
    path('account/register/', views.register, name='Register'),
    path('account/', views.account, name='Account'),
    path('account/logout/', views.logout_customer, name='Logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
