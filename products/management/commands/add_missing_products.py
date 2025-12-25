from django.core.management.base import BaseCommand
from products.models import Juice, Category
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add remaining 56 missing products to complete 124 total'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding missing products...')
        
        # Missing products data
        missing = [
            (35, "Detox Blend", "MIX FRUIT BLENDS", 90, "Orange + Ginger + Pineapple metabolism boost", "Orange, Pineapple, Ginger"),
            (46, "Apple Banana Smoothie", "CLASSIC SMOOTHIES (NO SUGAR)", 120, "Creamy natural blend", "Apple, Banana"),
            (49, "Strawberry Smoothie", "CLASSIC SMOOTHIES (NO SUGAR)", 130, "Berry antioxidant smoothie", "Strawberries, Banana"),
            (50, "Pine Apple Smoothie", "CLASSIC SMOOTHIES (NO SUGAR)", 120, "Tropical digestive aid", "Pineapple, Banana"),
            (51, "Sapota Banana Smoothie", "CLASSIC SMOOTHIES (NO SUGAR)", 120, "Caramel energy boost", "Sapota, Banana"),
            (52, "Dates Milk Shake", "DRYFRUIT MILKSHAKES", 130, "Iron-rich stamina", "Dates, Milk"),
            (55, "Kaju Anjeer Milkshake", "DRYFRUIT MILKSHAKES", 150, "Premium nuts and figs", "Cashews, Figs, Milk"),
            (58, "Kaju Badam Milkshake", "DRYFRUIT MILKSHAKES", 150, "Protein powerhouse", "Cashews, Almonds, Milk"),
            (59, "Kaju Milkshake", "DRYFRUIT MILKSHAKES", 140, "Creamy cashew delight", "Cashews, Milk"),
            (60, "Badam Pista Milkshake", "DRYFRUIT MILKSHAKES", 150, "Royal nut blend", "Almonds, Pistachios, Milk"),
            (63, "Zero Sugar Avil Milk", "KERALA SPECIALS AVIL MILKS", 120, "Traditional without sugar", "Avil, Banana, Milk"),
            (64, "Special Avil Milk", "KERALA SPECIALS AVIL MILKS", 150, "Extra loaded premium", "Avil, Banana, Milk, Nuts"),
            (67, "Dry Fruit Falooda", "FALOODA", 160, "Premium with dry fruits", "Milk, Rose, Vermic elli, Dry Fruits"),
            (68, "Kesar Falooda", "FALOODA", 160, "Aromatic saffron", "Milk, Saffron, Vermicelli"),
            (69, "Kesar Pista Falooda", "FALOODA", 170, "Saffron pistachio luxury", "Milk, Saffron, Pistachios"),
            (70, "Black Current Falooda", "FALOODA", 160, "Bold berry flavor", "Milk, Blackcurrant, Vermicelli"),
            (71, "Mango Falooda", "FALOODA", 160, "Summer mango delight", "Milk, Mango, Vermicelli"),
            (72, "Strawberry Mango Falooda", "FALOODA", 160, "Fruity fusion", "Milk, Strawberry, Mango"),
            (73, "Strawberry Falooda", "FALOODA", 160, "Classic pink berry", "Milk, Strawberry, Vermicelli"),
            (74, "Mix Fruit Falooda", "FALOODA", 160, "Assorted fruits", "Milk, Mixed Fruits, Vermicelli"),
            (75, "Kulfi Falooda", "FALOODA", 170, "Traditional kulfi", "Milk, Kulfi, Vermicelli"),
            (76, "Malai Kulfi Falooda", "FALOODA", 170, "Creamy malai kulfi", "Milk, Malai Kulfi, Vermicelli"),
            (77, "Dates Falooda", "FALOODA", 160, "Natural date sweetness", "Milk, Dates, Vermicelli"),
           (78, "Rainbow Falooda", "ICECREAMS FALOODA", 180, "Multi-layered treat", "Milk, Multi Syrups, Ice Cream"),
            (79, "Rainbow Kulfi Falooda", "ICECREAMS FALOODA", 180, "Vibrant kulfi", "Milk, Rainbow Kulfi"),
            (85, "Green Grapes Mojito", "THE MOJITO BAR", 100, "Sweet grape cooler", "Grapes, Lime, Mint"),
            (86, "Pomegranate Mojito", "THE MOJITO BAR", 110, "Ruby antioxidant", "Pomegranate, Lime, Mint"),
            (87, "Kiwi Mojito", "THE MOJITO BAR", 110, "Zesty tropical", "Kiwi, Lime, Mint"),
            (88, "Orange Crush", "THE MOJITO BAR", 100, "Citrus refresher", "Orange, Lime, Mint"),
            (89, "Strawberry Bliss", "THE MOJITO BAR", 100, "Sweet berry", "Strawberry, Lime, Mint"),
            (90, "Pineapple Mojito", "THE MOJITO BAR", 100, "Tropical island", "Pineapple, Lime, Mint"),
            (91, "Lychee Mojito", "THE MOJITO BAR", 110, "Exotic floral", "Lychee, Lime, Mint"),
            (92, "Passion Fruit Mojito", "THE MOJITO BAR", 110, "Intense tropical", "Passion Fruit, Lime, Mint"),
            (93, "Dragon Fruit Mojito", "THE MOJITO BAR", 110, "Pink superfood", "Dragon Fruit, Lime, Mint"),
            (94, "Peach Mojito", "THE MOJITO BAR", 100, "Soft velvety", "Peach, Lime, Mint"),
            (95, "Mango Mojito", "THE MOJITO BAR", 110, "King of mojitos", "Mango, Lime, Mint"),
            (96, "Pista Shake", "ICE CREAM MILK SHAKE", 120, "Aromatic pistachio", "Pistachio Ice Cream, Milk"),
            (97, "Kesar Pista Milkshake", "ICE CREAM MILK SHAKE", 140, "Royal saffron pistachio", "Saffron, Pistachio, Milk"),
            (98, "Black Currant Shake", "ICE CREAM MILK SHAKE", 120, "Bold berry shake", "Blackcurrant Ice Cream, Milk"),
            (99, "Cold Coffee", "ICE CREAM MILK SHAKE", 100, "Classic bold coffee", "Coffee, Milk"),
            (100, "Cold Coffee with Ice Cream", "ICE CREAM MILK SHAKE", 120, "Creamy coffee", "Coffee, Milk, Ice Cream"),
            (101, "Butterscotch Shake", "ICE CREAM MILK SHAKE", 120, "Crunchy caramel", "Butterscotch Ice Cream, Milk"),
            (106, "Avocado Cream", "CREAMY FRUIT DELIGHT", 150, "Rich superfood", "Avocado, Cream"),
            (107, "Mango Cream", "CREAMY FRUIT DELIGHT", 150, "Seasonal luxury", "Mango, Cream"),
            (108, "Mixed Berry Cream", "CREAMY FRUIT DELIGHT", 150, "Berry medley", "Mixed Berries, Cream"),
            (109, "Custard Apple Cream", "CREAMY FRUIT DELIGHT", 150, "Sitaphal special", "Custard Apple, Cream"),
            (110, "Strawberry Cream", "CREAMY FRUIT DELIGHT", 150, "Classic berry", "Strawberries, Cream"),
            (113, "Kiwi Cream", "CREAMY FRUIT DELIGHT", 150, "Tangy tropical", "Kiwi, Cream"),
            (114, "Chikku Cream", "CREAMY FRUIT DELIGHT", 140, "Caramel sapota", "Sapota, Cream"),
            (115, "Mix Fruit with Ice Cream", "FRUITS & SCOOPS", 140, "Seasonal with scoop", "Mixed Fruits, Ice Cream"),
            (116, "Seasonal Fruit with Ice Cream", "FRUITS & SCOOPS", 140, "Fresh season picks", "Seasonal Fruits, Ice Cream"),
            (117, "Dry Fruit with Ice Cream", "FRUITS & SCOOPS", 160, "Premium nuts", "Dry Fruits, Ice Cream"),
            (119, "Kiwi with Ice Cream", "FRUITS & SCOOPS", 150, "Tangy kiwi vanilla", "Kiwi, Ice Cream"),
            (120, "Mix Fruit Bowl", "FRUIT BOWLS", 120, "Fresh seasonal", "Mixed Seasonal Fruits"),
            (122, "Papaya bowl", "FRUIT BOWLS", 80, "Fresh papaya cubes", "Papaya"),
            (124, "Combo bowl (any 3 fruits)", "FRUIT BOWLS", 100, "Custom selection", "Customer Choice - 3 Fruits"),
        ]
        
        created = 0
        updated = 0
        
        for pid, name, cat_name, price, desc, ingred in missing:
            category, _ = Category.objects.get_or_create(name=cat_name)
            
            juice, created_now = Juice.objects.update_or_create(
                id=pid,
                defaults={
                    'name': name,
                    'category': category,
                    'description': desc,
                    'price': Decimal(str(price)),
                    'long_description': f'{desc}. Made with fresh ingredients.',
                    'net_quantity_ml': 300,
                    'features': ['Fresh', 'Natural', 'No Preservatives'],
                    'benefits': [{'title': 'Nutritious', 'description': 'Healthy choice'}],
                    'nutrition_calories': Decimal('150.00'),
                    'nutrition_total_fat': Decimal('2.0'),
                    'nutrition_carbohydrate': Decimal('30.0'),
                    'nutrition_dietary_fiber': Decimal('2.0'),
                    'nutrition_total_sugars': Decimal('20.0'),
                    'nutrition_protein': Decimal('3.0'),
                    'ingredients': ingred,
                    'allergen_info': 'Check with staff',
                    'is_active': True
                }
            )
            
            if created_now:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'CREATED: {name} (ID {pid})'))
            else:
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'UPDATED: {name} (ID {pid})'))
        
        self.stdout.write(self.style.SUCCESS(f'\nDone! Created: {created}, Updated: {updated}'))
        self.stdout.write(self.style.SUCCESS(f'Total products in DB should now be: 124'))
