from django.db import migrations


def normalize_legacy_model_name(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    Bike.objects.filter(slug='davidputtra-xc').update(name='DAVIDPUTTRA XC')


class Migration(migrations.Migration):
    dependencies = [('home', '0004_alter_bike_image_name_alter_bike_long_description_and_more')]
    operations = [migrations.RunPython(normalize_legacy_model_name, migrations.RunPython.noop)]
