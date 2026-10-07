from django.db import migrations


CITIES = [
    ('Kolkata', 'West Bengal', '22.572600', '88.363900'),
    ('Bengaluru (Bangalore)', 'Karnataka', '12.971600', '77.594600'),
    ('Mumbai', 'Maharashtra', '19.076000', '72.877700'),
    ('Delhi', 'NCT of Delhi', '28.613900', '77.209000'),
    ('Chandigarh', 'Chandigarh', '30.733300', '76.779400'),
    ('Lucknow', 'Uttar Pradesh', '26.846700', '80.946700'),
]


def seed_coverage_cities(apps, schema_editor):
    CoverageCity = apps.get_model('home', 'DealerCoverageCity')
    for city, region, latitude, longitude in CITIES:
        CoverageCity.objects.get_or_create(
            city=city,
            defaults={
                'region': region,
                'latitude': latitude,
                'longitude': longitude,
                'showroom_available': True,
                'service_center_available': True,
                'availability_note': 'City coverage shown; contact us for exact branch addresses and appointments.',
                'is_active': True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [('home', '0016_bike_rental_units')]
    operations = [migrations.RunPython(seed_coverage_cities, migrations.RunPython.noop)]
