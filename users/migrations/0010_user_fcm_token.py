# Generated for fcm_token field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_assigned_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcm_token',
            field=models.CharField(
                blank=True,
                help_text='Firebase Cloud Messaging device token for push notifications',
                max_length=255,
                null=True
            ),
        ),
    ]
