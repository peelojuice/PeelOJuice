from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Creates default superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email='peelojuice0@gmail.com',
                password='Admin@123',
                full_name='Purna Chandra Rao',
                phone_number='9876543210'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser created!'))
            self.stdout.write('Email: peelojuice0@gmail.com')
            self.stdout.write('Password: Admin@123')
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
