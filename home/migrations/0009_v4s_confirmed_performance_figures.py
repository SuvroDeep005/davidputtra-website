from django.db import migrations


def set_v4s_figures(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    Bike.objects.filter(slug='davidputtra-v4s').update(
        engine_cc=1000,
        power_bhp=140,
        torque_nm=150,
        long_description=(
            'The DAVIDPUTTRA V4S pairs dramatic red sports styling with a 1000 cc engine, '
            '140 bhp and 150 Nm of torque. Its fully faired profile, low windscreen and '
            'purposeful stance give it a focused road presence. Contact our team for '
            'availability and confirmed equipment details.'
        ),
        ride_story=(
            'With 140 bhp and 150 Nm from its 1000 cc engine, the V4S brings a clear '
            'performance profile to the DAVIDPUTTRA range. Book a test ride to experience '
            'its riding position and response for yourself.'
        ),
    )


class Migration(migrations.Migration):
    dependencies = [('home', '0008_bike_cooling_bike_engine_configuration_and_more')]
    operations = [migrations.RunPython(set_v4s_figures, migrations.RunPython.noop)]
