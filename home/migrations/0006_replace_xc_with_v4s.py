from django.db import migrations


def replace_xc_with_v4s(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    Bike.objects.filter(slug='davidputtra-xc').update(
        name='DAVIDPUTTRA V4S',
        slug='davidputtra-v4s',
        category='Supersport',
        description='A vivid supersport presence with a fully faired silhouette and a focused road-going character.',
        long_description='The DAVIDPUTTRA V4S brings a sharp, fully faired supersport look to the lineup. Its vivid red bodywork, low windscreen and purposeful stance give it an unmistakable presence. Published technical specifications and availability are being confirmed; contact our team for the latest information and to arrange a conversation about the bike.',
        design_story='The V4S stands apart through its full fairing, low windscreen and dramatic red finish. The result is a focused supersport silhouette designed to make a striking first impression.',
        ride_story='The V4S is presented as a sport-oriented addition to the DAVIDPUTTRA range. Final performance figures and equipment details are being confirmed, so speak with our team for current information and a test-ride update.',
        ideal_for='Riders drawn to fully faired supersport styling and a focused road presence.',
        image='bikes/davidputtra-v4s.webp',
        image_name='',
        engine_cc=0,
        power_bhp=0,
        torque_nm=0,
        badge='new',
        is_active=True,
    )


class Migration(migrations.Migration):
    dependencies = [('home', '0005_normalize_legacy_model_name')]
    operations = [migrations.RunPython(replace_xc_with_v4s, migrations.RunPython.noop)]
