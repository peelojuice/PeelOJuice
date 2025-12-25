from django.core.management.base import BaseCommand
from products.models import Branch, Juice, BranchProduct

class Command(BaseCommand):
    help = 'Setup product availability for all branches (all products available initially)'
    
    def handle(self, *args, **kwargs):
        branches = Branch.objects.filter(is_active=True)
        products = Juice.objects.filter(is_active=True)
        
        if not branches.exists():
            self.stdout.write(self.style.ERROR('No branches found! Run seed_branches first.'))
            return
        
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found! Make sure products are seeded.'))
            return
        
        created_count = 0
        
        for branch in branches:
            for product in products:
                _, created = BranchProduct.objects.get_or_create(
                    branch=branch,
                    product=product,
                    defaults={'is_available': True}
                )
                if created:
                    created_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Setup complete! Created {created_count} branch-product links'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total: {branches.count()} branches × {products.count()} products = {branches.count() * products.count()} links'
        ))
