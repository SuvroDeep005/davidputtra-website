from django.db import migrations


OLD_AND_NEW = {
    'heritage_intro': (
        'Born from Indian character, built for the open road.',
        'An Indian point of view, a clear sense of purpose, and a road still unfolding.',
    ),
    'heritage_story': (
        'DAVIDPUTTRA brings a distinct Indian identity to modern motorcycling. Each machine is shaped around the rider, the road and the moments that make a ride memorable.',
        'Every road asks something different of a motorcycle. From the close rhythm of city traffic to the open stretch beyond familiar places, riders look for confidence, character and a machine that feels their own.\n\nDAVIDPUTTRA is shaped around that idea. Our Indian perspective informs how we think about design and the riding experience: expressive machines, purposeful performance and a closer connection to the people who ride them. We keep looking forward while staying grounded in the spirit of the road.',
    ),
    'engineering_title': (
        'Precision in every detail.',
        'Precision in every detail.',
    ),
    'engineering_story': (
        'We pursue balanced performance through careful design, considered component choices and attention to the details riders feel every day.',
        'Precision engineering starts with a clear purpose. We consider how a motorcycle looks, feels and responds, then pay attention to the details that bring the whole experience together—from its stance and riding position to its power and everyday usability. Our aim is to balance expressive design with confidence-inspiring performance, and to share specifications clearly so riders can choose with confidence.',
    ),
    'satisfaction_title': (
        'Riders come first.',
        'Riders come first.',
    ),
    'satisfaction_story': (
        'From the first enquiry to ongoing service, we aim to make every interaction clear, responsive and worthy of the trust riders place in us.',
        'Customer care should feel as personal as the ride. We want it to be straightforward to explore the lineup, speak with our team, book a test ride and find service support. Clear information, attentive follow-up and a willingness to listen are the foundations of a better relationship with every rider.',
    ),
}


def expand_default_copy(apps, schema_editor):
    BrandContent = apps.get_model('home', 'BrandContent')
    for brand in BrandContent.objects.all():
        changed = []
        for field, (old, new) in OLD_AND_NEW.items():
            if getattr(brand, field) == old:
                setattr(brand, field, new)
                changed.append(field)
        if changed:
            brand.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [('home', '0010_alter_brandcontent_engineering_story_and_more')]
    operations = [migrations.RunPython(expand_default_copy, migrations.RunPython.noop)]
