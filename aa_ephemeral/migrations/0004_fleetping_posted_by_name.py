from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_ephemeral', '0003_fleetping_can_send_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleetping',
            name='posted_by_name',
            field=models.CharField(default='', help_text='Display name of the FC who posted the ping', max_length=100),
        ),
    ]
