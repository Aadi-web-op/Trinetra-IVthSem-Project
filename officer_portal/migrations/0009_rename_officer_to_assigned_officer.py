from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('officer_portal', '0008_chatmessage_case'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='officer',
            new_name='assigned_officer',
        ),
    ]
