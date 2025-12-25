from decimal import Decimal
from products.models import Category, Juice

MENU = {
    "PURE FRUIT JUICES": [
        ("Mango", 80),
        ("Muskmelon", 60),
        ("Papaya", 50),
        ("Pomegranate", 130),
        ("Orange", 60),
        ("Mosambi", 60),
        ("Grape", 50),
        ("Watermelon", 50),
        ("Pineapple", 80),
        ("Apple", 100),
        ("Kiwi", 120),
        ("Dragon Fruit", 120),
        ("Strawberry", 120),
        ("Carrot", 80),
        ("Beetroot", 80),
        ("ABC (Amla/Apple + Carrot + Beetroot)", 100),
        ("ABC with Ginger", 100),
    ],

    "FRUIT MILKSHAKES": [
        ("Muskmelon Milkshake", 50),
        ("Papaya Milkshake", 50),
        ("Pomegranate Milkshake", 90),
        ("Sapota Milkshake", 60),
        ("Sapota + Banana Milkshake", 70),
        ("Banana Milkshake", 50),
        ("Apple Milkshake", 80),
        ("Kiwi Milkshake", 110),
        ("Dragon Fruit Milkshake", 110),
        ("Strawberry Milkshake", 110),
        ("Avocado Milkshake", 150),
        ("Sithaphal Milkshake", 120),
        ("Carrot Milkshake", 70),
        ("Kannur Cocktail Milkshake (Papaya + Carrot)", 80),
    ],

    "MIX FRUIT BLENDS": [
        ("Anarkali (Pomegranate + Kiwi)", 130),
        ("Kiwi Cooler (Kiwi + Orange + Pine Apple)", 120),
        ("Watermelon Sunrise (Orange + Mint + Watermelon)", 90),
        ("Detox Blend (Orange + Ginger + Pine Apple)", 90),
        ("Immunity Booster (Pine Apple + Grape + Apple)", 90),
        ("Maramari (Pineapple + Mosambi)", 80),
        ("Vegetable Juice (Carrot, Beetroot & Cucumber)", 80),
        ("Ganga Jamuna Saraswathi (Orange + Musambi + Pine Apple)", 100),
        ("Ganga Jamuna (Orange + Musambi)", 80),
        ("Tropical Trio (Mango + Kiwi + Strawberry)", 140),
        ("Carronge (Carrot + Orange)", 100),
    ],

    "CLASSIC SMOOTHIES (NO SUGAR)": [
        ("Avocado Banana Smoothie", 140),
        ("Dry Fruit Smoothie", 150),
        ("Carrot Banana Smoothie", 120),
        ("Apple Banana Smoothie", 120),
        ("Mango Banana Smoothie", 130),
        ("Kiwi Blend Smoothie", 130),
        ("Strawberry Smoothie", 130),
        ("Pine Apple Smoothie", 120),
        ("Sapota Banana Smoothie", 100),
    ],

    "DRYFRUIT MILKSHAKES": [
        ("Dates Milk Shake", 130),
        ("Kesar Royal Milkshake", 150),
        ("Dryfruit Milkshake (anjeer)", 150),
        ("Kaju Anjeer Milkshake", 150),
        ("Kesar Badam Milkshake", 150),
        ("Kaju Badam Milkshake", 150),
        ("Kaju Milkshake", 150),
        ("Badam Pista Milkshake", 150),
    ],

    "KERALA SPECIALS AVIL MILKS": [
        ("Malabar Avil Milk", 120),
        ("Dry Fruit Avil Milk", 140),
        ("Fruit N Nut Avil Milk", 120),
        ("Zero Sugar Avil Milk", 120),
        ("Special Avil Milk", 150),
    ],

    "FALOODA": [
        ("Mumbai Special Falooda", 160),
        ("Dry Fruit Falooda", 130),
        ("Vanilla Falooda", 110),
        ("Kesar Falooda", 110),
        ("Butterscotch Falooda", 110),
        ("Black Current Falooda", 110),
        ("Mango Falooda", 110),
        ("Chocolate Falooda", 110),
        ("Strawberry Falooda", 110),
        ("Mix Fruit Falooda", 110),
        ("Kulfi Falooda", 110),
        ("Rose Falooda", 110),
        ("Dates Falooda", 110),
    ],

    "ICECREAMS FALOODA": [
        ("Rainbow Falooda", 130),
        ("Malabar Falooda", 120),
        ("Mango Kulfi Falooda", 120),
        ("Butterscotch Kulfi Falooda", 120),
        ("Kesar Pista Falooda", 120),
        ("Triple Falooda", 130),
    ],

    "THE MOJITO BAR": [
        ("Classic Mint Mojito", 100),
        ("Green Apple Fizz", 100),
        ("Blue Lagoon", 100),
        ("Fresh Lime Mojito", 100),
        ("Orange Crush", 100),
        ("Strawberry Bliss", 100),
        ("Blueberry Mojito", 110),
        ("Rose Mojito", 100),
    ],

    "ICE CREAM MILK SHAKE": [
        ("Vanilla Shake", 100),
        ("Strawberry Shake", 100),
        ("Chocolate Shake", 100),
        ("Butterscotch Shake", 100),
        ("Pista Shake", 100),
        ("Kesar Pista Milkshake", 120),
        ("Black Currant Shake", 100),
        ("Cold Coffee", 100),
        ("Cold Coffee with Ice Cream", 110),
        ("Oreo Milk Shake", 110),
        ("Kitkat Shake", 110),
        ("Rose Milkshake", 90),
    ],

    "CREAMY FRUIT DELIGHT": [
        ("Mix Fruit Cream", 130),
        ("Avocado Cream", 150),
        ("Dry Fruit Cream", 150),
        ("Mango Cream", 150),
        ("Custard Apple Cream (Sitaphal)", 150),
        ("Strawberry Cream", 150),
        ("Dragon Fruit Cream", 150),
        ("Chocolate Cream", 140),
        ("Kitkat Cream", 150),
        ("Kiwi Cream", 150),
        ("Chikku Cream", 140),
    ],

    "FRUITS & SCOOPS": [
        ("Mix Fruit with Ice Cream", 130),
        ("Mango with Ice Cream", 150),
        ("Dry Fruit with Ice Cream", 150),
        ("Dragon Fruit with Ice Cream", 150),
        ("Kiwi with Ice Cream", 150),
    ],

    "FRUIT BOWLS": [
        ("Mix Fruit Bowl", 120),
        ("Watermelon bowl", 80),
        ("Papaya bowl", 80),
        ("Muskmelon bowl", 80),
        ("Combo bowl (any 3 fruits)", 90),
    ],
}


def run():
    for category_name, juices in MENU.items():

        category, created = Category.objects.get_or_create(
            name=category_name
        )

        for juice_name, price in juices:
            Juice.objects.get_or_create(
                name=juice_name,
                category=category,
                defaults={
                    "price": Decimal(price),
                    "is_active": True
                }
            )   

    print("SUCCESS: Initial juice menu seeded successfully")
