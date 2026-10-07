from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify
import django.db.models.deletion
import django.core.validators


def add_starter_content(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    BrandContent = apps.get_model('home', 'BrandContent')
    bikes = [
        {
            'name': 'DAVIDPUTTRA XS', 'slug': 'davidputtra-xs', 'category': 'Born to dominate',
            'description': 'Compact, aggressive and designed for everyday dominance.',
            'long_description': 'A confident everyday machine with a 650 cc engine, 45 BHP and 50 Nm of torque. Its compact character makes city rides feel natural while keeping the weekend road in reach.',
            'engine_cc': 650, 'power_bhp': 45, 'torque_nm': 50,
            'image_name': 'davidputtra-xs.jpg', 'badge': 'bestseller', 'sort_order': 1,
        },
        {
            'name': 'DAVIDPUTTRA 850V', 'slug': 'davidputtra-850v', 'category': 'Ignite the road',
            'description': 'A sharper step up in performance with an unmistakable street presence.',
            'long_description': 'An 850 cc motorcycle with 70 BHP and 80 Nm, built for riders looking for stronger mid-range presence and a more focused road experience.',
            'engine_cc': 850, 'power_bhp': 70, 'torque_nm': 80,
            'image_name': 'davidputtra-850V.jpg', 'badge': 'new', 'sort_order': 2,
        },
        {
            'name': 'DAVIDPUTTRA ADV', 'slug': 'davidputtra-adv', 'category': 'Ride into the night',
            'description': 'The flagship machine for riders who refuse to settle.',
            'long_description': 'The 1000 cc flagship pairs 110 BHP with 130 Nm for a commanding ride. Explore the details and request a ride to experience it for yourself.',
            'engine_cc': 1000, 'power_bhp': 110, 'torque_nm': 130,
            'image_name': 'davidputtra-adv.jpg', 'badge': 'flagship', 'sort_order': 3,
        },
    ]
    for values in bikes:
        Bike.objects.update_or_create(slug=values['slug'], defaults=values)
    BrandContent.objects.get_or_create(pk=1)


def normalize_existing_slugs(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    used = set(Bike.objects.exclude(slug='').values_list('slug', flat=True))
    for bike in Bike.objects.filter(slug='').order_by('pk'):
        base = slugify(bike.name) or f'bike-{bike.pk}'
        slug = base
        suffix = 2
        while slug in used:
            slug = f'{base}-{suffix}'
            suffix += 1
        bike.slug = slug
        bike.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(model_name='bike', name='slug', field=models.SlugField(blank=True, db_index=False, default='', max_length=110)),
        migrations.AddField(model_name='bike', name='long_description', field=models.TextField(blank=True, default='')),
        migrations.AddField(model_name='bike', name='engine_cc', field=models.PositiveIntegerField(default=0, verbose_name='Engine (cc)')),
        migrations.AddField(model_name='bike', name='power_bhp', field=models.PositiveIntegerField(default=0, verbose_name='Power (BHP)')),
        migrations.AddField(model_name='bike', name='torque_nm', field=models.PositiveIntegerField(default=0, verbose_name='Torque (Nm)')),
        migrations.AddField(model_name='bike', name='image_name', field=models.CharField(blank=True, default='', help_text='Optional existing file name in the static folder.', max_length=120)),
        migrations.AddField(model_name='bike', name='sort_order', field=models.PositiveSmallIntegerField(default=0)),
        migrations.AddField(model_name='bike', name='is_active', field=models.BooleanField(default=True)),
        migrations.AlterModelOptions(name='bike', options={'ordering': ('sort_order', 'name')}),
        migrations.AlterField(model_name='bike', name='image', field=models.ImageField(blank=True, upload_to='bikes/')),
        migrations.AlterField(model_name='bike', name='price', field=models.DecimalField(decimal_places=2, default=0, max_digits=10)),
        migrations.AlterField(model_name='booking', name='bike', field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.bike')),
        migrations.AlterField(model_name='booking', name='phone', field=models.CharField(max_length=20)),
        migrations.AddField(model_name='booking', name='customer', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        migrations.AddField(model_name='booking', name='preferred_date', field=models.DateField(blank=True, null=True)),
        migrations.AddField(model_name='booking', name='location', field=models.CharField(blank=True, default='', max_length=150)),
        migrations.AddField(model_name='booking', name='status', field=models.CharField(choices=[('requested', 'Request received'), ('pending_payment', 'Pending payment'), ('confirmed', 'Confirmed'), ('payment_failed', 'Payment failed')], default='requested', max_length=20)),
        migrations.AddField(model_name='booking', name='razorpay_order_id', field=models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField(model_name='booking', name='razorpay_payment_id', field=models.CharField(blank=True, default='', max_length=100)),
        migrations.CreateModel(
            name='BrandContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heritage_intro', models.CharField(default='Born from Indian character, built for the open road.', max_length=240)),
                ('heritage_story', models.TextField(default='DAVIDPUTTRA brings a distinct Indian identity to modern motorcycling. Each machine is shaped around the rider, the road and the moments that make a ride memorable.')),
                ('engineering_title', models.CharField(default='Precision in every detail.', max_length=120)),
                ('engineering_story', models.TextField(default='We pursue balanced performance through careful design, considered component choices and attention to the details riders feel every day.')),
                ('satisfaction_title', models.CharField(default='Riders come first.', max_length=120)),
                ('satisfaction_story', models.TextField(default='From the first enquiry to ongoing service, we aim to make every interaction clear, responsive and worthy of the trust riders place in us.')),
            ],
        ),
        migrations.CreateModel(
            name='DealerLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('location_type', models.CharField(choices=[('showroom', 'Showroom'), ('service', 'Service center')], max_length=20)),
                ('address', models.CharField(max_length=240)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(blank=True, max_length=100, verbose_name='State / region')),
                ('postal_code', models.CharField(blank=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Required to place this location on the map.', max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Required to place this location on the map.', max_digits=9, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ('city', 'name')},
        ),
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('review', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('location', models.CharField(blank=True, max_length=100)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bike', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.bike')),
            ],
            options={'ordering': ('-created_at',)},
        ),
        migrations.RunPython(normalize_existing_slugs, migrations.RunPython.noop),
        migrations.RunPython(add_starter_content, migrations.RunPython.noop),
        migrations.AlterField(model_name='bike', name='slug', field=models.SlugField(blank=True, db_index=False, max_length=110, unique=True)),
    ]
