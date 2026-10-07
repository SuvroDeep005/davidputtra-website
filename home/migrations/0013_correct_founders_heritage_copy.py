from django.db import migrations


def correct_founders_copy(apps, schema_editor):
    BrandContent = apps.get_model('home', 'BrandContent')
    BrandContent.objects.filter(
        founders_story__contains='brand started by Suvro, Roumo and Pramit',
    ).update(
        founders_story=(
            'DAVIDPUTTRA is a West Bengal-based motorcycle brand founded by three friends: '
            'Suvro, Roumo and Pramit. All three are passionate riders. Their shared love of '
            'motorcycles inspired them to create a brand shaped by an Indian point of view '
            'and a close connection to riders.'
        ),
    )


class Migration(migrations.Migration):
    dependencies = [('home', '0012_brandcontent_founders_names_and_more')]
    operations = [migrations.RunPython(correct_founders_copy, migrations.RunPython.noop)]
