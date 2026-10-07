from django.db import migrations


def update_v4s_copy(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    Bike.objects.filter(slug='davidputtra-v4s').update(
        category='Naked Sports',
        description='A vivid red sports machine with a focused, road-going character.',
        long_description='The DAVIDPUTTRA V4S brings bold red styling and sharp sporting proportions to the lineup. Its purposeful stance gives it a distinct presence on the road. Published technical specifications and availability are being confirmed; contact our team for the latest information and to arrange a conversation about the bike.',
        design_story='Striking red styling and a focused sport-bike silhouette give the V4S a strong identity in the range. The details come together to make a confident first impression.',
        ride_story='The V4S is presented as a sport-oriented addition to the DAVIDPUTTRA range. Final performance figures and equipment details are being confirmed, so speak with our team for current information and a test-ride update.',
        ideal_for='Riders drawn to bold sports styling and a focused road presence.',
    )


class Migration(migrations.Migration):
    dependencies = [('home', '0006_replace_xc_with_v4s')]
    operations = [migrations.RunPython(update_v4s_copy, migrations.RunPython.noop)]
