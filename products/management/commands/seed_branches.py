from django.core.management.base import BaseCommand
from products.models import Branch

class Command(BaseCommand):
    help = 'Seed initial branches (3 Bangalore locations)'
    
    def handle(self, *args, **kwargs):
        branches_data = [
            {
                'name': 'PeelOJuice MG Road',
                'address': '123, MG Road, Commercial Street',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001',
                'phone': '+91 80 1234 5678',
                'email': 'mgroad@peelojuice.com',
                'opening_time': '09:00:00',
                'closing_time': '22:00:00',
                'is_active': True,
            },
            {
                'name': 'PeelOJuice Koramangala',
                'address': '456, 5th Block, Koramangala',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560034',
                'phone': '+91 80 8765 4321',
                'email': 'koramangala@peelojuice.com',
                'opening_time': '09:00:00',
                'closing_time': '22:00:00',
                'is_active': True,
            },
            {
                'name': 'PeelOJuice Indiranagar',
                'address': '789, 100 Feet Road, Indiranagar',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560038',
                'phone': '+91 80 9999 8888',
                'email': 'indiranagar@peelojuice.com',
                'opening_time': '09:00:00',
                'closing_time': '22:00:00',
                'is_active': True,
            },
        ]
        
        for branch_data in branches_data:
            branch, created = Branch.objects.get_or_create(
                name=branch_data['name'],
                defaults=branch_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created branch: {branch.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'- Branch already exists: {branch.name}'))
        
        total_branches = Branch.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal active branches: {total_branches}'))
