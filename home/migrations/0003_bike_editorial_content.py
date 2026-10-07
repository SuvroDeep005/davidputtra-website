from django.db import migrations, models


def add_model_stories(apps, schema_editor):
    Bike = apps.get_model('home', 'Bike')
    stories = {
        'davidputtra-xs': {
            'description': 'A confident everyday machine with a compact stance and a character all its own.',
            'long_description': 'The DAVIDPUTTRA XS pairs a 650 cc engine with 45 BHP and 50 Nm of torque. Its compact proportions suit daily city routes, while its road-focused character makes a longer weekend ride feel right at home. A distinctive entry into the range for riders who want their everyday motorcycle to feel anything but ordinary.',
            'design_story': 'Compact proportions and a purposeful silhouette give the XS its street-ready character. Its restrained shape keeps the focus on the ride and gives the model a clear identity in the DAVIDPUTTRA lineup.',
            'ride_story': 'With 45 BHP and 50 Nm from its 650 cc engine, the XS brings a balanced performance profile to everyday riding. The published figures offer a useful starting point; book a ride to experience the engine and ergonomics for yourself.',
            'ideal_for': 'Riders looking for one distinctive motorcycle for everyday journeys and open-road weekends.',
        },
        'davidputtra-850v': {
            'description': 'A performance-led step up, shaped for riders ready to take the long way home.',
            'long_description': 'The DAVIDPUTTRA 850V brings an 850 cc engine, 70 BHP and 80 Nm of torque to a confident, road-focused package. It is positioned for riders seeking a stronger step up in the range, with the presence for open roads and the composure to make each journey feel deliberate. Visit a showroom to explore its design and riding position.',
            'design_story': 'The 850V makes a direct visual statement, with a focused stance and contemporary street presence. Its place in the lineup is clear: a bolder, more performance-oriented expression of the DAVIDPUTTRA character.',
            'ride_story': 'An 850 cc engine with 70 BHP and 80 Nm gives the 850V a clear performance profile on paper. A test ride is the best way to understand its response, riding position and how it feels on your roads.',
            'ideal_for': 'Riders ready to move up to a more performance-focused motorcycle for city-to-highway journeys.',
        },
        'davidputtra-adv': {
            'description': 'The flagship expression of the range, made for riders who want every journey to feel significant.',
            'long_description': 'At the top of the DAVIDPUTTRA range, the ADV pairs a 1000 cc engine with 110 BHP and 130 Nm of torque. Its adventure-oriented identity and commanding profile are made for riders drawn to longer routes and changing horizons. Explore the details in person and speak with our team about the right setup for your journeys.',
            'design_story': 'An adventure-inspired silhouette gives the ADV its unmistakable flagship presence. Every line reinforces its place at the top of the range and its invitation to look beyond the familiar route.',
            'ride_story': 'The ADV pairs 110 BHP and 130 Nm with a 1000 cc engine. Those headline figures tell one part of the story; arrange a test ride to assess the riding position and overall character for yourself.',
            'ideal_for': 'Experienced riders drawn to the flagship experience, longer journeys and an adventure-led outlook.',
        },
        'davidputtra-xc': {
            'description': 'A compact sports cruiser with an assertive stance and an easy everyday attitude.',
            'long_description': 'The DAVIDPUTTRA XC brings a sports-cruiser perspective to the lineup. Its compact, aggressive character is designed to make daily journeys feel distinctive while keeping the open road in view. Published engine and performance figures are not yet available; contact our team for the latest information.',
            'design_story': 'The XC pairs a compact profile with a sports-cruiser attitude. Its visual character is assertive without losing the approachable proportions that make it feel at home in an everyday lineup.',
            'ride_story': 'The XC is positioned as an everyday sports cruiser. Final technical specifications are still being confirmed, so speak with the team for current details and availability.',
            'ideal_for': 'Riders interested in a distinctive sports-cruiser profile for everyday use.',
        },
    }
    for slug, content in stories.items():
        Bike.objects.filter(slug=slug).update(**content)


class Migration(migrations.Migration):
    dependencies = [('home', '0002_dynamic_site_and_checkout')]
    operations = [
        migrations.AddField(model_name='bike', name='design_story', field=models.TextField(blank=True, help_text='Design details shown on the model page.')),
        migrations.AddField(model_name='bike', name='ride_story', field=models.TextField(blank=True, help_text='Describe the riding character without adding unverified specifications.')),
        migrations.AddField(model_name='bike', name='ideal_for', field=models.CharField(blank=True, help_text='A short rider profile, such as city-to-weekend riding.', max_length=220)),
        migrations.RunPython(add_model_stories, migrations.RunPython.noop),
    ]
