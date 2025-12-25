from django.core.management.base import BaseCommand
from products.models import Juice, Category
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed all 124 products with complete details'

    def get_all_products(self):
        return [
            # PURE FRUIT JUICES (1-17)
            {
                'id': 1, 'name': 'Mango', 'category': 'PURE FRUIT JUICES',
                'description': 'A rich and creamy blend of premium mangoes that captures the essence of tropical sunshine.',
                'price': 80.00,
                'long_description': "Made from handpicked Alfonso mangoes, this juice delivers a smooth, velvety texture with natural sweetness. Rich in vitamins A and C, it's a delicious way to boost your immunity and satisfy your tropical cravings.",
                'net_quantity_ml': 300,
                'features': ['100% Pure Fruit', 'No Added Sugar', 'Vitamin Rich', 'Fresh Daily'],
                'benefits': [
                    {'title': 'Immune Support', 'description': 'High in Vitamin C to strengthen your body defenses.'},
                    {'title': 'Eye Health', 'description': 'Rich in Vitamin A and beta-carotene for vision support.'},
                    {'title': 'Natural Energy', 'description': 'Natural fruit sugars provide sustained energy throughout the day.'}
                ],
                'nutrition_calories': 135.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 35.0,
                'nutrition_dietary_fiber': 1.6, 'nutrition_total_sugars': 31.0, 'nutrition_protein': 0.8,
                'ingredients': 'Fresh Mango',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 2, 'name': 'Muskmelon', 'category': 'PURE FRUIT JUICES',
                'description': 'A light and refreshing juice from sweet muskmelon, perfect for hydration on warm days.',
                'price': 60.00,
                'long_description': "This cooling juice is extracted from ripe muskmelons, offering a subtle sweetness and high water content. It's naturally hydrating and packed with essential minerals that help regulate body temperature.",
                'net_quantity_ml': 300,
                'features': ['Hydrating', 'Low Calorie', 'Mineral Rich', 'Cooling Effect'],
                'benefits': [
                    {'title': 'Hydration Boost', 'description': 'High water content keeps you refreshed and hydrated.'},
                    {'title': 'Digestive Health', 'description': 'Natural fiber aids in smooth digestion.'},
                    {'title': 'Skin Glow', 'description': 'Vitamins promote healthy, radiant skin.'}
                ],
                'nutrition_calories': 64.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 16.0,
                'nutrition_dietary_fiber': 0.9, 'nutrition_total_sugars': 14.0, 'nutrition_protein': 0.8,
                'ingredients': 'Fresh Muskmelon',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 3, 'name': 'Papaya', 'category': 'PURE FRUIT JUICES',
                'description': 'A smooth and naturally sweet juice from ripe papaya, excellent for digestion.',
                'price': 50.00,
                'long_description': "Extracted from perfectly ripened papayas, this juice contains papain enzymes that aid digestion. Its creamy texture and mild sweetness make it a breakfast favorite that's gentle on the stomach.",
                'net_quantity_ml': 300,
                'features': ['Enzyme Rich', 'Digestive Aid', 'Natural Sweetness', 'Stomach Friendly'],
                'benefits': [
                    {'title': 'Digestive Enzyme', 'description': 'Papain helps break down proteins for better digestion.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Natural compounds reduce inflammation.'},
                    {'title': 'Heart Health', 'description': 'Fiber and antioxidants support cardiovascular wellness.'}
                ],
                'nutrition_calories': 55.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 14.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 11.0, 'nutrition_protein': 0.6,
                'ingredients': 'Fresh Papaya',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 4, 'name': 'Pomegranate', 'category': 'PURE FRUIT JUICES',
                'description': 'A premium antioxidant-rich juice extracted from ruby-red pomegranate arils.',
                'price': 130.00,
                'long_description': "Hand-extracted from fresh pomegranate seeds, this jewel-toned juice is packed with powerful antioxidants. Known for its heart-healthy properties and tangy-sweet flavor, it's a nutritional powerhouse in every glass.",
                'net_quantity_ml': 300,
                'features': ['Antioxidant Powerhouse', 'Heart Healthy', 'Premium Quality', 'Hand Extracted'],
                'benefits': [
                    {'title': 'Cardiovascular Support', 'description': 'Helps maintain healthy blood pressure and circulation.'},
                    {'title': 'Antioxidant Protection', 'description': 'Fights free radicals and cellular damage.'},
                    {'title': 'Memory Enhancement', 'description': 'Studies suggest benefits for cognitive function.'}
                ],
                'nutrition_calories': 134.00, 'nutrition_total_fat': 1.2, 'nutrition_carbohydrate': 32.0,
                'nutrition_dietary_fiber': 0.3, 'nutrition_total_sugars': 24.0, 'nutrition_protein': 2.0,
                'ingredients': 'Fresh Pomegranate',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 5, 'name': 'Orange', 'category': 'PURE FRUIT JUICES',
                'description': 'Classic freshly squeezed orange juice bursting with Vitamin C and citrus tang.',
                'price': 60.00,
                'long_description': "Squeezed from sun-ripened oranges, this juice delivers a perfect balance of sweetness and tartness. It's your daily dose of Vitamin C in the most delicious form, supporting immunity and overall vitality.",
                'net_quantity_ml': 300,
                'features': ['Vitamin C Rich', 'Freshly Squeezed', 'Immune Booster', 'Classic Favorite'],
                'benefits': [
                    {'title': 'Immune Defense', 'description': 'High Vitamin C content strengthens immunity.'},
                    {'title': 'Collagen Production', 'description': 'Supports healthy skin and tissue repair.'},
                    {'title': 'Energy Boost', 'description': 'Natural sugars provide quick, healthy energy.'}
                ],
                'nutrition_calories': 112.00, 'nutrition_total_fat': 0.5, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 0.5, 'nutrition_total_sugars': 21.0, 'nutrition_protein': 1.7,
                'ingredients': 'Fresh Orange',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 6, 'name': 'Mosambi', 'category': 'PURE FRUIT JUICES',
                'description': 'A mild and soothing sweet lime juice, gentle on the stomach and refreshing.',
                'price': 60.00,
                'long_description': "Extracted from Indian sweet limes, this juice offers a gentler citrus experience. It's less acidic than regular limes, making it perfect for sensitive stomachs while still providing excellent Vitamin C.",
                'net_quantity_ml': 300,
                'features': ['Low Acidity', 'Gentle Citrus', 'Stomach Friendly', 'Vitamin Rich'],
                'benefits': [
                    {'title': 'Gentle Digestion', 'description': 'Low acid content makes it easy on the stomach.'},
                    {'title': 'Vitamin Boost', 'description': 'Rich in Vitamin C without harsh acidity.'},
                    {'title': 'Natural Coolant', 'description': 'Helps cool the body naturally.'}
                ],
                'nutrition_calories': 86.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 0.8, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 0.7,
                'ingredients': 'Fresh Mosambi (Sweet Lime)',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 7, 'name': 'Grape', 'category': 'PURE FRUIT JUICES',
                'description': 'Sweet and tangy juice from fresh grapes, loaded with natural antioxidants.',
                'price': 50.00,
                'long_description': "Pressed from fresh grapes, this juice combines natural sweetness with a hint of tartness. Rich in resveratrol and other antioxidants, it's as healthy as it is delicious.",
                'net_quantity_ml': 300,
                'features': ['Antioxidant Rich', 'Natural Sweetness', 'Heart Healthy', 'Resveratrol Source'],
                'benefits': [
                    {'title': 'Heart Protection', 'description': 'Resveratrol supports cardiovascular health.'},
                    {'title': 'Anti-Aging', 'description': 'Antioxidants combat signs of aging.'},
                    {'title': 'Brain Health', 'description': 'Compounds support cognitive function.'}
                ],
                'nutrition_calories': 152.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 39.0,
                'nutrition_dietary_fiber': 0.3, 'nutrition_total_sugars': 36.0, 'nutrition_protein': 0.6,
                'ingredients': 'Fresh Grapes',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 8, 'name': 'Watermelon', 'category': 'PURE FRUIT JUICES',
                'description': 'Ultra-hydrating juice from juicy watermelon, perfect for beating the heat.',
                'price': 50.00,
                'long_description': "Made from fresh, ripe watermelon, this juice is nature's sports drink. With over 90% water content and natural electrolytes, it's the ultimate thirst quencher that keeps you cool and refreshed.",
                'net_quantity_ml': 300,
                'features': ['Ultra Hydrating', 'Electrolyte Rich', 'Low Calorie', 'Natural Coolant'],
                'benefits': [
                    {'title': 'Maximum Hydration', 'description': 'High water content rapidly rehydrates the body.'},
                    {'title': 'Muscle Recovery', 'description': 'Contains amino acids that aid muscle recovery.'},
                    {'title': 'Weight Management', 'description': 'Low in calories but high in volume and satisfaction.'}
                ],
                'nutrition_calories': 71.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 18.0,
                'nutrition_dietary_fiber': 0.6, 'nutrition_total_sugars': 15.0, 'nutrition_protein': 1.4,
                'ingredients': 'Fresh Watermelon',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 9, 'name': 'Pineapple', 'category': 'PURE FRUIT JUICES',
                'description': 'Tropical and tangy pineapple juice with digestive enzymes and vibrant flavor.',
                'price': 80.00,
                'long_description': "Freshly extracted from golden pineapples, this juice is packed with bromelain, a natural enzyme that aids digestion. Its sweet-tart flavor and tropical aroma transport you to paradise with every sip.",
                'net_quantity_ml': 300,
                'features': ['Enzyme Rich', 'Tropical Flavor', 'Anti-Inflammatory', 'Digestive Aid'],
                'benefits': [
                    {'title': 'Digestive Support', 'description': 'Bromelain enzymes help break down proteins.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Natural compounds reduce inflammation.'},
                    {'title': 'Immune Boost', 'description': 'High in Vitamin C and manganese.'}
                ],
                'nutrition_calories': 133.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 33.0,
                'nutrition_dietary_fiber': 0.7, 'nutrition_total_sugars': 25.0, 'nutrition_protein': 0.9,
                'ingredients': 'Fresh Pineapple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 10, 'name': 'Apple', 'category': 'PURE FRUIT JUICES',
                'description': 'Crisp and refreshing apple juice made from fresh apples, a timeless classic.',
                'price': 100.00,
                'long_description': "Pressed from premium apples, this juice offers a perfect balance of sweetness and crispness. Rich in polyphenols and pectin, it's not just delicious but also supports heart health and digestion.",
                'net_quantity_ml': 300,
                'features': ['Polyphenol Rich', 'Heart Healthy', 'Natural Pectin', 'Classic Taste'],
                'benefits': [
                    {'title': 'Heart Health', 'description': 'Pectin and polyphenols support cardiovascular wellness.'},
                    {'title': 'Digestive Support', 'description': 'Natural fiber aids gut health.'},
                    {'title': 'Blood Sugar Balance', 'description': 'Helps regulate glucose levels when consumed in moderation.'}
                ],
                'nutrition_calories': 117.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 0.6, 'nutrition_total_sugars': 24.0, 'nutrition_protein': 0.3,
                'ingredients': 'Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 11, 'name': 'Kiwi', 'category': 'PURE FRUIT JUICES',
                'description': 'Exotic and tangy kiwi juice, exceptionally rich in Vitamin C and antioxidants.',
                'price': 120.00,
                'long_description': "Extracted from fresh kiwi fruits, this bright green juice packs more Vitamin C than oranges. Its unique tangy-sweet flavor and exceptional nutrient density make it a premium wellness choice.",
                'net_quantity_ml': 300,
                'features': ['Vitamin C Powerhouse', 'Exotic Flavor', 'Antioxidant Rich', 'Premium Fruit'],
                'benefits': [
                    {'title': 'Immunity Super Boost', 'description': 'Contains twice the Vitamin C of oranges.'},
                    {'title': 'Digestive Enzyme', 'description': 'Actinidin enzyme aids protein digestion.'},
                    {'title': 'Sleep Quality', 'description': 'Contains serotonin which may improve sleep.'}
                ],
                'nutrition_calories': 122.00, 'nutrition_total_fat': 1.0, 'nutrition_carbohydrate': 29.0,
                'nutrition_dietary_fiber': 3.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 2.2,
                'ingredients': 'Fresh Kiwi',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 12, 'name': 'Dragon Fruit', 'category': 'PURE FRUIT JUICES',
                'description': 'Exotic and visually stunning juice from dragon fruit, mild and refreshing.',
                'price': 120.00,
                'long_description': "Made from vibrant dragon fruit, this juice offers a subtle sweetness and striking appearance. Rich in antioxidants and prebiotics, it's as beneficial for your gut health as it is beautiful to look at.",
                'net_quantity_ml': 300,
                'features': ['Exotic Superfruit', 'Prebiotic Rich', 'Antioxidant Loaded', 'Visually Stunning'],
                'benefits': [
                    {'title': 'Gut Health', 'description': 'Prebiotics support beneficial gut bacteria.'},
                    {'title': 'Blood Sugar Control', 'description': 'May help regulate blood sugar levels.'},
                    {'title': 'Antioxidant Protection', 'description': 'Betacyanins fight oxidative stress.'}
                ],
                'nutrition_calories': 102.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 1.8, 'nutrition_total_sugars': 20.0, 'nutrition_protein': 1.8,
                'ingredients': 'Fresh Dragon Fruit',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 13, 'name': 'Strawberry', 'category': 'PURE FRUIT JUICES',
                'description': 'Sweet and aromatic strawberry juice bursting with flavor and Vitamin C.',
                'price': 120.00,
                'long_description': "Crafted from fresh, ripe strawberries, this juice captures the essence of summer. Its natural sweetness, vibrant color, and high antioxidant content make it both a treat and a health boost.",
                'net_quantity_ml': 300,
                'features': ['Antioxidant Rich', 'Natural Sweetness', 'Vitamin Packed', 'Premium Berries'],
                'benefits': [
                    {'title': 'Heart Health', 'description': 'Anthocyanins support cardiovascular function.'},
                    {'title': 'Blood Sugar Management', 'description': 'May help regulate blood sugar response.'},
                    {'title': 'Skin Health', 'description': 'Vitamin C promotes collagen production.'}
                ],
                'nutrition_calories': 97.00, 'nutrition_total_fat': 0.6, 'nutrition_carbohydrate': 23.0,
                'nutrition_dietary_fiber': 2.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 1.3,
                'ingredients': 'Fresh Strawberry',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 14, 'name': 'Carrot', 'category': 'PURE FRUIT JUICES',
                'description': 'Fresh carrot juice loaded with beta-carotene for eye health and immunity.',
                'price': 80.00,
                'long_description': "Freshly extracted from premium carrots, this vibrant orange juice is a vision superfood. Packed with beta-carotene that converts to Vitamin A, it supports eye health, skin glow, and immune function.",
                'net_quantity_ml': 300,
                'features': ['Beta-Carotene Rich', 'Eye Health', 'Skin Glow', 'Immune Support'],
                'benefits': [
                    {'title': 'Vision Support', 'description': 'High Vitamin A content promotes healthy eyesight.'},
                    {'title': 'Skin Radiance', 'description': 'Beta-carotene gives skin a natural glow.'},
                    {'title': 'Immune Function', 'description': 'Supports the body natural defenses.'}
                ],
                'nutrition_calories': 94.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 1.9, 'nutrition_total_sugars': 13.0, 'nutrition_protein': 2.2,
                'ingredients': 'Fresh Carrot',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 15, 'name': 'Beetroot', 'category': 'PURE FRUIT JUICES',
                'description': 'Earthy and nutrient-dense beetroot juice, excellent for stamina and vitality.',
                'price': 80.00,
                'long_description': "Extracted from fresh beetroots, this deep ruby juice is a natural performance enhancer. Rich in nitrates that improve blood flow, it's popular among athletes and health enthusiasts for boosting stamina and endurance.",
                'net_quantity_ml': 300,
                'features': ['Nitrate Rich', 'Stamina Booster', 'Blood Pressure Support', 'Athletic Performance'],
                'benefits': [
                    {'title': 'Enhanced Endurance', 'description': 'Nitrates improve oxygen delivery to muscles.'},
                    {'title': 'Blood Pressure', 'description': 'May help lower blood pressure naturally.'},
                    {'title': 'Detoxification', 'description': 'Supports liver detoxification processes.'}
                ],
                'nutrition_calories': 87.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 20.0,
                'nutrition_dietary_fiber': 2.8, 'nutrition_total_sugars': 16.0, 'nutrition_protein': 3.3,
                'ingredients': 'Fresh Beetroot',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 16, 'name': 'ABC (Amla/Apple + Carrot + Beetroot)', 'category': 'PURE FRUIT JUICES',
                'description': 'A powerful wellness blend combining apple/amla, carrot, and beetroot for immunity.',
                'price': 100.00,
                'long_description': "This legendary health tonic combines three nutritional powerhouses. The synergy of apple's antioxidants, carrot's beta-carotene, and beetroot's nitrates creates a comprehensive wellness drink that supports immunity, vitality, and overall health.",
                'net_quantity_ml': 300,
                'features': ['Triple Power', 'Immunity Booster', 'Detoxifying', 'Complete Wellness'],
                'benefits': [
                    {'title': 'Comprehensive Nutrition', 'description': 'Three superfoods in one powerful blend.'},
                    {'title': 'Immune Support', 'description': 'Multiple vitamins and minerals boost immunity.'},
                    {'title': 'Energy & Vitality', 'description': 'Natural nutrients provide sustained energy.'}
                ],
                'nutrition_calories': 93.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 2.2, 'nutrition_total_sugars': 16.0, 'nutrition_protein': 2.0,
                'ingredients': 'Fresh Apple or Amla, Fresh Carrot, Fresh Beetroot',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 17, 'name': 'ABC with Ginger', 'category': 'PURE FRUIT JUICES',
                'description': 'The classic ABC blend enhanced with warming ginger for extra immune support.',
                'price': 100.00,
                'long_description': "Taking the powerful ABC blend to the next level, this version adds fresh ginger for its anti-inflammatory and digestive properties. The warming spice complements the sweet earthiness while amplifying health benefits.",
                'net_quantity_ml': 300,
                'features': ['Triple Power Plus Ginger', 'Anti-Inflammatory', 'Digestive Support', 'Warming Effect'],
                'benefits': [
                    {'title': 'Enhanced Immunity', 'description': 'Ginger adds powerful anti-inflammatory compounds.'},
                    {'title': 'Digestive Comfort', 'description': 'Ginger soothes and aids digestion.'},
                    {'title': 'Circulation Boost', 'description': 'Warming properties improve blood flow.'}
                ],
                'nutrition_calories': 96.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 23.0,
                'nutrition_dietary_fiber': 2.3, 'nutrition_total_sugars': 16.0, 'nutrition_protein': 2.0,
                'ingredients': 'Fresh Apple or Amla, Fresh Carrot, Fresh Beetroot, Fresh Ginger',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },

            # FRUIT MILKSHAKES (18-23)
            {
                'id': 18, 'name': 'Muskmelon Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A creamy and cooling milkshake with sweet muskmelon and fresh milk.',
                'price': 50.00,
                'long_description': "Blending ripe muskmelon with chilled milk creates this refreshing treat. The natural sweetness of the fruit combines perfectly with creamy milk for a beverage that's both satisfying and hydrating.",
                'net_quantity_ml': 300,
                'features': ['Creamy', 'Naturally Sweet', 'Cooling', 'Calcium Rich'],
                'benefits': [
                    {'title': 'Hydration', 'description': 'High water content keeps you refreshed.'},
                    {'title': 'Calcium Boost', 'description': 'Milk provides essential calcium for bones.'},
                    {'title': 'Gentle Energy', 'description': 'Natural sugars and protein provide balanced energy.'}
                ],
                'nutrition_calories': 165.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 0.9, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 6.0,
                'ingredients': 'Fresh Muskmelon, Fresh Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 19, 'name': 'Papaya Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'Smooth and creamy papaya blended with milk for digestive wellness.',
                'price': 50.00,
                'long_description': "This gentle milkshake combines enzyme-rich papaya with nourishing milk. It's easy on the stomach while providing sustained energy, making it an ideal breakfast or post-workout drink.",
                'net_quantity_ml': 300,
                'features': ['Enzyme Rich', 'Stomach Friendly', 'Creamy Texture', 'Digestive Aid'],
                'benefits': [
                    {'title': 'Digestive Support', 'description': 'Papain enzymes aid protein digestion.'},
                    {'title': 'Nutrient Absorption', 'description': 'Milk fat helps absorb fat-soluble vitamins.'},
                    {'title': 'Sustained Energy', 'description': 'Protein and carbs provide lasting fuel.'}
                ],
                'nutrition_calories': 156.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 6.0,
                'ingredients': 'Fresh Papaya, Fresh Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 20, 'name': 'Pomegranate Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A luxurious blend of antioxidant-rich pomegranate with creamy milk.',
                'price': 90.00,
                'long_description': "This premium milkshake combines the ruby richness of pomegranate with smooth milk. The tangy-sweet fruit beautifully balances the creaminess, creating an indulgent yet healthy treat.",
                'net_quantity_ml': 300,
                'features': ['Antioxidant Powerhouse', 'Premium Ingredients', 'Heart Healthy', 'Creamy Indulgence'],
                'benefits': [
                    {'title': 'Cardiovascular Health', 'description': 'Pomegranate supports heart function.'},
                    {'title': 'Bone Strength', 'description': 'Calcium from milk builds strong bones.'},
                    {'title': 'Antioxidant Protection', 'description': 'Fights free radical damage.'}
                ],
                'nutrition_calories': 235.00, 'nutrition_total_fat': 6.0, 'nutrition_carbohydrate': 40.0,
                'nutrition_dietary_fiber': 0.3, 'nutrition_total_sugars': 32.0, 'nutrition_protein': 7.0,
                'ingredients': 'Fresh Pomegranate, Fresh Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 21, 'name': 'Sapota Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A naturally sweet and creamy milkshake from rich sapota (chikoo) fruit.',
                'price': 60.00,
                'long_description': "Sapota's caramel-like sweetness blends perfectly with milk in this indulgent shake. No added sugar needed – the fruit's natural sweetness creates a dessert-like experience that's actually nutritious.",
                'net_quantity_ml': 300,
                'features': ['Naturally Sweet', 'No Added Sugar', 'Energy Boost', 'Caramel Notes'],
                'benefits': [
                    {'title': 'Natural Energy', 'description': 'High natural sugar content provides quick energy.'},
                    {'title': 'Bone Health', 'description': 'Rich in calcium and phosphorus.'},
                    {'title': 'Digestive Fiber', 'description': 'Supports healthy digestion.'}
                ],
                'nutrition_calories': 218.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 40.0,
                'nutrition_dietary_fiber': 4.0, 'nutrition_total_sugars': 35.0, 'nutrition_protein': 6.0,
                'ingredients': 'Fresh Sapota (Chikoo), Fresh Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 22, 'name': 'Sapota + Banana Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A power-packed combination of sapota and banana for maximum energy.',
                'price': 70.00,
                'long_description': "This dynamic duo creates an ultra-creamy, naturally sweet shake that's perfect for athletes and active individuals. The combination provides sustained energy, potassium, and satisfying thickness.",
                'net_quantity_ml': 300,
                'features': ['Double Fruit Power', 'Ultra Creamy', 'High Energy', 'Potassium Rich'],
                'benefits': [
                    {'title': 'Sustained Energy', 'description': 'Complex carbs from both fruits provide lasting fuel.'},
                    {'title': 'Muscle Function', 'description': 'Potassium supports muscle health.'},
                    {'title': 'Post-Workout Recovery', 'description': 'Ideal protein and carb ratio for recovery.'}
                ],
                'nutrition_calories': 268.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 52.0,
                'nutrition_dietary_fiber': 5.0, 'nutrition_total_sugars': 44.0, 'nutrition_protein': 7.0,
                'ingredients': 'Fresh Sapota (Chikoo), Fresh Banana, Fresh Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 23, 'name': 'Banana Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'Classic creamy banana milkshake, a timeless favorite for all ages.',
                'price': 50.00,
                'long_description': "The ultimate comfort drink that never goes out of style. Ripe bananas blended with fresh milk create this thick, creamy shake that's naturally sweet and incredibly satisfying.",
                'net_quantity_ml': 300,
                'features': ['Classic Favorite', 'Ultra Creamy', 'Naturally Sweet', 'Kid-Friendly'],
                'benefits': [
                    {'title': 'Instant Energy', 'description': 'Quick-digesting carbs provide immediate fuel.'},
                    {'title': 'Mood Booster', 'description': 'Tryptophan helps produce serotonin.'},
                    {'title': 'Digestive Health', 'description': 'Pectin fiber supports gut health.'}
                ],
                'nutrition_calories': 213.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 38.0,
                'nutrition_dietary_fiber': 3.0, 'nutrition_total_sugars': 31.0, 'nutrition_protein': 7.0,
                'ingredients': 'Fresh Banana, Fresh Milk',
                'allergen_info': 'Contains Milk'
            },

            # FRUIT MILKSHAKES continued (24-32)
            {
                'id': 24, 'name': 'Apple Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A smooth and creamy classic. Crisp apples blended with chilled milk for a comforting, nutritious treat.',
                'price': 80.00,
                'long_description': 'Our Apple Milkshake is made by blending premium red apples with farm-fresh milk. It retains the pectin and fiber of the apple while adding the protein and calcium of dairy. It is a perfect breakfast-on-the-go or a healthy afternoon snack.',
                'net_quantity_ml': 300,
                'features': ['Freshly Blended', 'Creamy Texture', 'Rich in Calcium', 'No Preservatives', 'Naturally Filling'],
                'benefits': [
                    {'title': 'Bone Strength', 'description': 'High calcium content from fresh milk supports skeletal health.'},
                    {'title': 'Sustained Energy', 'description': 'The combination of fruit carbs and dairy protein provides long-lasting energy.'},
                    {'title': 'Heart Health', 'description': 'Apple polyphenols contribute to healthy cardiovascular function.'}
                ],
                'nutrition_calories': 175.00, 'nutrition_total_fat': 4.2, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 2.0, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 5.8,
                'ingredients': 'Fresh Apple, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 25, 'name': 'Sapota Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'Naturally malty, sweet, and incredibly rich. Often described as liquid caramel, this shake is a favorite for those with a sweet tooth.',
                'price': 60.00,
                'long_description': 'Made with perfectly ripened Sapota (Chikku), this milkshake offers a unique, slightly grainy texture and a deep, earthy sweetness. It is naturally high in calories and fiber, making it an excellent energy booster.',
                'net_quantity_ml': 300,
                'features': ['High Energy', 'Caramel-like Taste', 'Fiber Rich', 'No Preservatives', 'Naturally Sweet'],
                'benefits': [
                    {'title': 'Digestive Health', 'description': 'High dietary fiber helps in maintaining a healthy digestive tract.'},
                    {'title': 'Instant Energy', 'description': 'Rich in natural fructose and sucrose for an immediate stamina lift.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Sapota is known for its high tannin content which has anti-inflammatory properties.'}
                ],
                'nutrition_calories': 195.00, 'nutrition_total_fat': 4.8, 'nutrition_carbohydrate': 35.0,
                'nutrition_dietary_fiber': 3.5, 'nutrition_total_sugars': 28.0, 'nutrition_protein': 4.5,
                'ingredients': 'Fresh Sapota (Chikku), Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 26, 'name': 'Kiwi Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A refreshing, tangy-sweet dairy blend. A unique tropical shake that is light on the stomach and high in Vitamin C.',
                'price': 110.00,
                'long_description': 'We blend zesty green kiwis with chilled milk to create a refreshing green shake. The tartness of the kiwi balances perfectly with the creaminess of the milk, providing a high-antioxidant treat.',
                'net_quantity_ml': 300,
                'features': ['Tangy & Sweet', 'Antioxidant Rich', 'Vitamin C Boost', 'No Preservatives', 'Unique Flavor'],
                'benefits': [
                    {'title': 'Immune Support', 'description': 'Excellent source of Vitamin C to help fight seasonal illnesses.'},
                    {'title': 'Skin Health', 'description': 'Antioxidants help in maintaining youthful and clear skin.'},
                    {'title': 'Metabolic Health', 'description': 'Rich in minerals like Potassium and Magnesium.'}
                ],
                'nutrition_calories': 165.00, 'nutrition_total_fat': 4.0, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 2.5, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 5.2,
                'ingredients': 'Fresh Kiwi, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 27, 'name': 'Strawberry Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'The ultimate berry indulgence. Made with real, fresh strawberries—not syrups—for an authentic, refreshing taste.',
                'price': 110.00,
                'long_description': 'Unlike commercial shakes, our Strawberry Milkshake uses real crushed strawberries blended with rich milk. It has a beautiful natural pink hue and is packed with Vitamin C and manganese.',
                'net_quantity_ml': 300,
                'features': ['Real Berries', 'No Artificial Colors', 'No Syrups', 'Anti-oxidant Rich', 'Always Fresh'],
                'benefits': [
                    {'title': 'Heart Health', 'description': 'Strawberries contain anthocyanins which support cardiac health.'},
                    {'title': 'Mood Enhancer', 'description': 'The natural sweetness and vitamin profile help in uplifting mood.'},
                    {'title': 'Low Glycemic Index', 'description': 'Provides a sweet experience with a lower impact on blood sugar compared to artificial shakes.'}
                ],
                'nutrition_calories': 180.00, 'nutrition_total_fat': 4.3, 'nutrition_carbohydrate': 29.0,
                'nutrition_dietary_fiber': 1.8, 'nutrition_total_sugars': 23.0, 'nutrition_protein': 5.0,
                'ingredients': 'Fresh Strawberries, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 28, 'name': 'Dragon Fruit Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'An exotic, visually stunning shake. A mild, creamy flavor with a beautiful magenta color and tiny, crunchy seeds.',
                'price': 110.00,
                'long_description': 'This shake is made using 100% fresh Pink Dragon Fruit. It is low in calories but high in nutrients, offering a silky texture with the subtle crunch of dragon fruit seeds, which are rich in healthy fats.',
                'net_quantity_ml': 300,
                'features': ['Superfood Shake', 'Exotic Look', 'Mildly Sweet', 'No Preservatives', 'Nutrient Dense'],
                'benefits': [
                    {'title': 'Healthy Seeds', 'description': 'The seeds provide essential Omega-3 and Omega-9 fatty acids.'},
                    {'title': 'Iron Boost', 'description': 'Helps in improving blood oxygen levels naturally.'},
                    {'title': 'High Antioxidants', 'description': 'Contains betalains which protect the body cells from oxidative stress.'}
                ],
                'nutrition_calories': 170.00, 'nutrition_total_fat': 4.6, 'nutrition_carbohydrate': 27.0,
                'nutrition_dietary_fiber': 2.8, 'nutrition_total_sugars': 20.0, 'nutrition_protein': 5.5,
                'ingredients': 'Fresh Dragon Fruit, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 29, 'name': 'Avocado Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'The ultimate creamy superfood shake. Silky smooth Avocado blended with chilled milk for a rich, buttery experience.',
                'price': 150.00,
                'long_description': 'A powerhouse of healthy monounsaturated fats. Because of its naturally thick consistency, it feels like a premium dessert but remains a healthy, nutrient-dense meal option that keeps you full for hours.',
                'net_quantity_ml': 300,
                'features': ['Heart Healthy', 'Ultra Creamy', 'No Added Sugar', 'No Preservatives', 'Superfood Base'],
                'benefits': [
                    {'title': 'Omega-3 Source', 'description': 'Excellent for brain health and maintaining healthy cholesterol levels.'},
                    {'title': 'Weight Management', 'description': 'High satiety levels help reduce cravings and keep you full longer.'},
                    {'title': 'Vitamin E Rich', 'description': 'Promotes healthy skin and protects cells from oxidative damage.'}
                ],
                'nutrition_calories': 210.00, 'nutrition_total_fat': 12.0, 'nutrition_carbohydrate': 18.0,
                'nutrition_dietary_fiber': 4.5, 'nutrition_total_sugars': 12.0, 'nutrition_protein': 5.8,
                'ingredients': 'Fresh Avocado, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 30, 'name': 'Pomegranate Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A vibrant, antioxidant-packed dairy blend. The sweet-tart flavor of pomegranate seeds meets the silkiness of fresh milk.',
                'price': 90.00,
                'long_description': 'We extract the juice from premium pomegranate arils and blend it instantly with chilled milk. This ensures a fresh, refreshing taste that provides a massive boost of antioxidants and vitamins.',
                'net_quantity_ml': 300,
                'features': ['Antioxidant Rich', 'Always Fresh', 'No Artificial Colors', 'No Preservatives', 'Tangy & Sweet'],
                'benefits': [
                    {'title': 'Heart Health', 'description': 'Pomegranate is known to support blood flow and arterial health.'},
                    {'title': 'Immunity Boost', 'description': 'High in Vitamin C and Vitamin K for overall body defense.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Helps in reducing systemic inflammation and improves joint health.'}
                ],
                'nutrition_calories': 185.00, 'nutrition_total_fat': 4.2, 'nutrition_carbohydrate': 32.0,
                'nutrition_dietary_fiber': 0.8, 'nutrition_total_sugars': 26.0, 'nutrition_protein': 5.1,
                'ingredients': 'Fresh Pomegranate Juice/Arils, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 31, 'name': 'Muskmelon Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'A hydrating and fragrant summer classic. Sweet cantaloupe blended with milk for a light yet creamy refreshment.',
                'price': 50.00,
                'long_description': 'Using sun-ripened muskmelons, this shake is naturally aromatic and cooling. It is an ideal drink for hot afternoons, providing essential electrolytes and a smooth, mellow flavor.',
                'net_quantity_ml': 300,
                'features': ['Hydrating', 'Aromatic', 'Always Fresh', 'No Preservatives', 'Naturally Cooling'],
                'benefits': [
                    {'title': 'Natural Coolant', 'description': 'Helps in regulating body temperature and soothing the stomach.'},
                    {'title': 'Eye Health', 'description': 'Rich in Beta-carotene which supports healthy vision.'},
                    {'title': 'Skin Hydration', 'description': 'High water content and vitamins promote hydrated, glowing skin.'}
                ],
                'nutrition_calories': 155.00, 'nutrition_total_fat': 4.1, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 20.0, 'nutrition_protein': 4.9,
                'ingredients': 'Fresh Muskmelon, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 32, 'name': 'Papaya Milkshake', 'category': 'FRUIT MILKSHAKES',
                'description': 'Tropical, smooth, and digestive-friendly. A nutrient-dense shake that is gentle on the stomach and rich in flavor.',
                'price': 50.00,
                'long_description': 'Blending ripe, orange-fleshed papayas with milk creates a thick, custard-like consistency. It is a great way to enjoy the digestive enzymes of papaya in a delicious, creamy format.',
                'net_quantity_ml': 300,
                'features': ['Digestive Aid', 'Custard-like Texture', 'Always Fresh', 'No Preservatives', 'Naturally Sweet'],
                'benefits': [
                    {'title': 'Digestive Support', 'description': 'Contains papain enzymes that help in protein breakdown and digestion.'},
                    {'title': 'Vitamin A Source', 'description': 'Supports immune function and helps maintain healthy mucous membranes.'},
                    {'title': 'Rich in Lycopene', 'description': 'Powerful antioxidant that protects cells from damage.'}
                ],
                'nutrition_calories': 170.00, 'nutrition_total_fat': 4.3, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 3.0, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 5.3,
                'ingredients': 'Fresh Papaya, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },

            # MIX FRUIT BLENDS (33-43)
            {
                'id': 33, 'name': 'Anarkali', 'category': 'MIX FRUIT BLENDS',
                'description': 'A royal blend of Pomegranate and Kiwi. Deep sweetness meets zesty tang for a refreshing, high-vitamin experience.',
                'price': 130.00,
                'long_description': 'One of our signature blends, Anarkali combines the ruby-red antioxidants of pomegranate with the sharp, green zest of kiwi. It is a beautifully balanced, no-sugar-added drink that is as healthy as it is flavorful.',
                'net_quantity_ml': 300,
                'features': ['Signature Blend', 'No Added Sugar', 'Antioxidant Duo', 'Always Fresh', 'No Preservatives'],
                'benefits': [
                    {'title': 'Skin Radiance', 'description': 'High Vitamin C and K promote collagen production and clear skin.'},
                    {'title': 'Immune Shield', 'description': 'Dual fruit vitamins provide superior defense against infections.'},
                    {'title': 'Blood Health', 'description': 'Iron-boosting pomegranate helps in maintaining healthy hemoglobin.'}
                ],
                'nutrition_calories': 115.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 2.2, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 1.4,
                'ingredients': 'Fresh Pomegranate, Fresh Kiwi',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 34, 'name': 'Kiwi Cooler', 'category': 'MIX FRUIT BLENDS',
                'description': 'A refreshing tropical zing! A sharp and zesty blend of Kiwi and Apple designed to wake up your taste buds.',
                'price': 120.00,
                'long_description': 'The Kiwi Cooler is our go-to for instant refreshment. By blending the tartness of green kiwis with the natural sweetness of apples, we have created a light, crisp beverage that is perfect for rehydrating on a hot day.',
                'net_quantity_ml': 300,
                'features': ['Zesty & Crisp', 'No Added Sugar', 'Vitamin C Packed', 'Always Fresh', 'Hydrating'],
                'benefits': [
                    {'title': 'Metabolic Spark', 'description': 'The tartness of kiwi helps stimulate digestive enzymes.'},
                    {'title': 'Antioxidant Boost', 'description': 'Protects your cells from oxidative stress and fatigue.'},
                    {'title': 'Low Calorie Refreshment', 'description': 'A lighter alternative to heavy shakes that does not compromise on flavor.'}
                ],
                'nutrition_calories': 108.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 3.8, 'nutrition_total_sugars': 20.0, 'nutrition_protein': 1.2,
                'ingredients': 'Fresh Kiwi, Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 36, 'name': 'Detox Blend', 'category': 'MIX FRUIT BLENDS',
                'description': 'Cleanse from within. A powerful green and red blend designed to flush out toxins and reset your system.',
                'price': 90.00,
                'long_description': 'Our Detox Blend is a carefully balanced mix of Beetroot, Carrot, and Apple. It is specifically formulated to support liver function and improve skin clarity by providing a concentrated dose of vitamins and nitrates in a delicious, easy-to-drink format.',
                'net_quantity_ml': 300,
                'features': ['System Reset', 'No Added Sugar', 'Rich in Nitrates', 'Always Fresh', 'Liver Support'],
                'benefits': [
                    {'title': 'Internal Cleansing', 'description': 'Helps the body naturally eliminate waste and toxins.'},
                    {'title': 'Skin Clarity', 'description': 'Reduces inflammation which often leads to clearer, brighter skin.'},
                    {'title': 'Enhanced Circulation', 'description': 'Beetroot nitrates help improve blood flow throughout the body.'}
                ],
                'nutrition_calories': 95.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 23.0,
                'nutrition_dietary_fiber': 4.2, 'nutrition_total_sugars': 17.0, 'nutrition_protein': 1.8,
                'ingredients': 'Fresh Beetroot, Fresh Carrot, Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 37, 'name': 'Ganga Jamuna Saraswathi', 'category': 'MIX FRUIT BLENDS',
                'description': 'A legendary trio. A harmonious blend of Mosambi (Sweet Lime), Orange, and Pineapple for a massive citrus hit.',
                'price': 100.00,
                'long_description': 'Named after the confluence of three rivers, this blend is a powerhouse of Vitamin C. It combines the mild sweetness of Mosambi, the classic tang of Orange, and the tropical punch of Pineapple. It is the ultimate immunity-boosting juice.',
                'net_quantity_ml': 300,
                'features': ['Citrus Powerhouse', 'No Added Sugar', 'Vitamin C Loaded', 'Always Fresh', 'Triple Blend'],
                'benefits': [
                    {'title': 'Immune Fortress', 'description': 'Triple the citrus means triple the protection for your immune system.'},
                    {'title': 'Digestion Aid', 'description': 'Natural acids and pineapple enzymes support a healthy gut.'},
                    {'title': 'Refreshing Electrolytes', 'description': 'Helps balance body salts and keeps you energized.'}
                ],
                'nutrition_calories': 110.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 27.0,
                'nutrition_dietary_fiber': 1.2, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 1.5,
                'ingredients': 'Fresh Mosambi, Fresh Orange, Fresh Pineapple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 38, 'name': 'Watermelon Pineapple Blend', 'category': 'MIX FRUIT BLENDS',
                'description': 'Pure summer hydration. The watery sweetness of watermelon meets the zesty tropical flavor of pineapple.',
                'price': 80.00,
                'long_description': 'This blend is designed for maximum thirst quenching. Watermelon provides high water content and lycopene, while pineapple adds a tart edge and bromelain, making it a perfect post-workout or mid-day refresher.',
                'net_quantity_ml': 300,
                'features': ['Ultra Hydrating', 'No Added Sugar', 'Tropical Mix', 'Always Fresh', 'Light & Easy'],
                'benefits': [
                    {'title': 'Muscle Recovery', 'description': 'Watermelon contains L-citrulline which may help reduce muscle soreness.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Bromelain from pineapple helps reduce body inflammation.'},
                    {'title': 'Low Calorie', 'description': 'A guilt-free way to satisfy a sweet craving.'}
                ],
                'nutrition_calories': 88.00, 'nutrition_total_fat': 0.1, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 0.8, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 1.1,
                'ingredients': 'Fresh Watermelon, Fresh Pineapple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 39, 'name': 'Iron Booster', 'category': 'MIX FRUIT BLENDS',
                'description': 'For strength and vitality. A mineral-rich blend of Pomegranate and Apple designed to naturally improve your blood health.',
                'price': 100.00,
                'long_description': 'Our Iron Booster focuses on nutrient density. Pomegranate provides the iron and antioxidants, while Apple provides the fiber and a smooth base. This blend is particularly recommended for those looking to naturally support their hemoglobin levels.',
                'net_quantity_ml': 300,
                'features': ['Mineral Rich', 'No Added Sugar', 'Blood Health Focus', 'Always Fresh', 'Premium Quality'],
                'benefits': [
                    {'title': 'Healthy Blood', 'description': 'Supports iron absorption and healthy red blood cell production.'},
                    {'title': 'Cardiac Support', 'description': 'Polyphenols from both fruits support heart and arterial health.'},
                    {'title': 'Energy Lift', 'description': 'Fights fatigue by improving oxygen transport in the body.'}
                ],
                'nutrition_calories': 125.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 31.0,
                'nutrition_dietary_fiber': 1.8, 'nutrition_total_sugars': 25.0, 'nutrition_protein': 1.3,
                'ingredients': 'Fresh Pomegranate, Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 40, 'name': 'Vitamin C Booster', 'category': 'MIX FRUIT BLENDS',
                'description': 'The ultimate defensive shield. A sharp, tangy blend of Orange, Mosambi, and Kiwi designed to maximize your daily vitamin intake.',
                'price': 90.00,
                'long_description': 'This blend is a citrus powerhouse. By combining the three highest sources of natural Vitamin C in our menu, we have created a juice that not only refreshes but actively supports your body natural defense system against seasonal changes.',
                'net_quantity_ml': 300,
                'features': ['Immunity Focus', 'No Added Sugar', 'High Vitamin C', 'Always Fresh', 'Zesty Flavor'],
                'benefits': [
                    {'title': 'Immune Defense', 'description': 'High concentration of Ascorbic acid to strengthen white blood cells.'},
                    {'title': 'Collagen Support', 'description': 'Vitamin C is essential for skin elasticity and tissue repair.'},
                    {'title': 'Antioxidant Rich', 'description': 'Protects the body from free radical damage and oxidative stress.'}
                ],
                'nutrition_calories': 105.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 25.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 1.6,
                'ingredients': 'Fresh Orange, Fresh Mosambi, Fresh Kiwi',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 41, 'name': 'Tropical Punch', 'category': 'MIX FRUIT BLENDS',
                'description': 'A vacation in a bottle. A lush blend of Mango, Pineapple, and a hint of Apple for a thick, exotic refreshment.',
                'price': 100.00,
                'long_description': 'This blend brings together the heavy, sweet notes of sun-ripened mango with the acidic spark of pineapple. It is a dense, flavorful juice that provides a massive energy boost and a taste of the tropics.',
                'net_quantity_ml': 300,
                'features': ['Exotic Flavor', 'No Added Sugar', 'Naturally Thick', 'Always Fresh', 'Energy Rich'],
                'benefits': [
                    {'title': 'Natural Energy', 'description': 'Rich in fruit sugars and minerals for a sustained energy release.'},
                    {'title': 'Digestive Enzymes', 'description': 'Pineapple bromelain aids in breaking down proteins effectively.'},
                    {'title': 'Vitamin A Boost', 'description': 'Mango provides high levels of carotenoids for healthy vision.'}
                ],
                'nutrition_calories': 135.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 33.0,
                'nutrition_dietary_fiber': 1.8, 'nutrition_total_sugars': 27.0, 'nutrition_protein': 1.2,
                'ingredients': 'Fresh Mango, Fresh Pineapple, Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 42, 'name': 'Beet-Apple Energizer', 'category': 'MIX FRUIT BLENDS',
                'description': 'Stamina and sweetness combined. A clean, earthy blend of Beetroot and Apple that supports endurance and blood health.',
                'price': 100.00,
                'long_description': 'Perfect as a pre-workout drink, this blend uses the nitrates from beetroot to improve oxygen flow and the natural sugars of apple for energy. It has a smooth, balanced taste that masks the intense earthiness of plain beetroot.',
                'net_quantity_ml': 300,
                'features': ['Pre-Workout Choice', 'No Added Sugar', 'Nitrate Rich', 'Always Fresh', 'Blood Support'],
                'benefits': [
                    {'title': 'Enhanced Endurance', 'description': 'Helps improve oxygen uptake during physical activity.'},
                    {'title': 'Blood Flow', 'description': 'Supports healthy circulation and cardiovascular function.'},
                    {'title': 'Detox Support', 'description': 'Aids the liver in flushing out toxins from the bloodstream.'}
                ],
                'nutrition_calories': 98.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 2.5, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 1.8,
                'ingredients': 'Fresh Beetroot, Fresh Apple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 43, 'name': 'Skin Glow Blend', 'category': 'MIX FRUIT BLENDS',
                'description': 'Beauty from within. A hydrating and antioxidant-rich mix of Carrot, Apple, and Orange designed for radiant skin.',
                'price': 100.00,
                'long_description': 'This blend focuses on skin-loving nutrients. Beta-carotene from carrots, polyphenols from apples, and Vitamin C from oranges work together to promote collagen production and protect the skin from environmental damage.',
                'net_quantity_ml': 300,
                'features': ['Beauty Focus', 'No Added Sugar', 'Beta-Carotene Rich', 'Always Fresh', 'Antioxidant Duo'],
                'benefits': [
                    {'title': 'UV Protection', 'description': 'Antioxidants help protect skin cells from sun-induced damage.'},
                    {'title': 'Complexion Support', 'description': 'Promotes a natural, healthy glow by purifying the blood.'},
                    {'title': 'Hydration', 'description': 'Keeps skin cells hydrated and plump from the inside out.'}
                ],
                'nutrition_calories': 92.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 23.0,
                'nutrition_dietary_fiber': 2.8, 'nutrition_total_sugars': 17.0, 'nutrition_protein': 1.4,
                'ingredients': 'Fresh Carrot, Fresh Apple, Fresh Orange',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },

            # CLASSIC SMOOTHIES (NO SUGAR) (44)
            {
                'id': 44, 'name': 'Avocado Banana Smoothie', 'category': 'CLASSIC SMOOTHIES (NO SUGAR)',
                'description': 'The ultimate creamy powerhouse. A thick, meal-replacement style smoothie that is rich in healthy fats and potassium.',
                'price': 140.00,
                'long_description': 'By blending the buttery texture of avocado with the natural sweetness of bananas, we have created a smoothie that is incredibly filling and smooth. It contains no added sugar, relying entirely on the banana for sweetness and the avocado for creaminess.',
                'net_quantity_ml': 300,
                'features': ['High Satiety', 'No Added Sugar', 'Creamy & Thick', 'Always Fresh', 'Healthy Fats'],
                'benefits': [
                    {'title': 'Brain & Heart Health', 'description': 'Rich in Omega-3 and healthy monounsaturated fats.'},
                    {'title': 'Sustained Fullness', 'description': 'Fiber and healthy fats prevent hunger pangs for hours.'},
                    {'title': 'Potassium Rich', 'description': 'Supports healthy blood pressure and nerve function.'}
                ],
                'nutrition_calories': 220.00, 'nutrition_total_fat': 12.5, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 6.2, 'nutrition_total_sugars': 14.0, 'nutrition_protein': 2.8,
                'ingredients': 'Fresh Avocado, Fresh Banana',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },

            # CLASSIC SMOOTHIES continued (45-48)
            {
                'id': 45, 'name': 'Dry Fruit Smoothie', 'category': 'CLASSIC SMOOTHIES (NO SUGAR)',
                'description': 'A naturally sweet, energy-packed blend. Features soaked dates and figs blended with a fruit base for a rich, mineral-heavy treat.',
                'price': 150.00,
                'long_description': 'Designed for those who need a stamina boost without refined sugar. We use high-quality dates and figs to provide a deep, caramel-like sweetness and a thick, satisfying texture that keeps you energized throughout the day.',
                'net_quantity_ml': 300,
                'features': ['Iron Rich', 'No Added Sugar', 'Natural Stamina', 'No Preservatives', 'Fiber Dense'],
                'benefits': [
                    {'title': 'Natural Stamina', 'description': 'High mineral content improves overall physical endurance.'},
                    {'title': 'Iron Booster', 'description': 'Dates and figs are excellent natural sources of iron for blood health.'},
                    {'title': 'Gut Health', 'description': 'High fiber content supports digestive regularity and gut health.'}
                ],
                'nutrition_calories': 210.00, 'nutrition_total_fat': 1.5, 'nutrition_carbohydrate': 48.0,
                'nutrition_dietary_fiber': 4.8, 'nutrition_total_sugars': 38.0, 'nutrition_protein': 2.8,
                'ingredients': 'Dates, Figs (Anjeer), Banana Base',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 47, 'name': 'Apple Banana Smoothie', 'category': 'CLASSIC SMOOTHIES (NO SUGAR)',
                'description': 'A sweet and comforting classic. The crispness of apples meets the creaminess of bananas for a perfectly balanced morning blend.',
                'price': 120.00,
                'long_description': 'This is a gentle, nourishing smoothie. It combines the pectin-rich benefits of apples with the potassium of bananas to create a drink that is easy on the stomach and provides a steady release of natural fruit energy.',
                'net_quantity_ml': 300,
                'features': ['Gentle on Stomach', 'No Added Sugar', 'Silky Texture', 'Always Fresh', 'Kid Friendly'],
                'benefits': [
                    {'title': 'Digestive Ease', 'description': 'Both fruits are soothing for the gut and easy to digest.'},
                    {'title': 'Heart Health', 'description': 'Contains apple polyphenols and potassium for cardiovascular support.'},
                    {'title': 'Mood Support', 'description': 'Vitamin B6 from bananas helps in natural mood regulation.'}
                ],
                'nutrition_calories': 140.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 34.0,
                'nutrition_dietary_fiber': 3.5, 'nutrition_total_sugars': 24.0, 'nutrition_protein': 1.6,
                'ingredients': 'Fresh Apple, Fresh Banana',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 48, 'name': 'Mango Banana Smoothie', 'category': 'CLASSIC SMOOTHIES (NO SUGAR)',
                'description': 'A tropical duo that is naturally thick and luscious. The rich sweetness of mango meets the smooth energy of banana.',
                'price': 130.00,
                'long_description': 'This no-sugar smoothie relies entirely on the natural sugars of sun-ripened mangoes. It is a high-fiber, high-potassium blend that serves as a perfect refreshing breakfast or pre-workout meal.',
                'net_quantity_ml': 300,
                'features': ['Tropical Mix', 'No Added Sugar', 'High Potassium', 'No Preservatives', 'Creamy Finish'],
                'benefits': [
                    {'title': 'Immune Support', 'description': 'High in Vitamin A and C to boost the body natural defenses.'},
                    {'title': 'Natural Energy', 'description': 'Steady glucose release from complex fruit fibers.'},
                    {'title': 'Vision Health', 'description': 'Rich in carotenoids from mangoes for eye protection.'}
                ],
                'nutrition_calories': 155.00, 'nutrition_total_fat': 0.4, 'nutrition_carbohydrate': 38.0,
                'nutrition_dietary_fiber': 3.2, 'nutrition_total_sugars': 28.0, 'nutrition_protein': 1.8,
                'ingredients': 'Fresh Mango, Fresh Banana',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },

            # DRYFRUIT MILKSHAKES (53-57)
            {
                'id': 53, 'name': 'Dates Milk Shake', 'category': 'DRYFRUIT MILKSHAKES',
                'description': 'Naturally sweet and iron-rich. Premium dates blended with farm-fresh milk for a traditional strength-building drink.',
                'price': 130.00,
                'long_description': 'Our Dates Milkshake is an ancient recipe for stamina. We use soft, high-quality dates that melt into the milk, providing a caramel-like flavor without a single grain of added refined sugar.',
                'net_quantity_ml': 300,
                'features': ['Iron Powerhouse', 'No Added Sugar', 'High Stamina', 'No Preservatives', 'Natural Sweetener'],
                'benefits': [
                    {'title': 'Hemoglobin Support', 'description': 'Helps improve iron levels and fights fatigue naturally.'},
                    {'title': 'Bone Health', 'description': 'Combined calcium from milk and minerals from dates.'},
                    {'title': 'Sustained Stamina', 'description': 'Perfect for physical recovery and long-lasting energy.'}
                ],
                'nutrition_calories': 210.00, 'nutrition_total_fat': 4.5, 'nutrition_carbohydrate': 42.0,
                'nutrition_dietary_fiber': 3.5, 'nutrition_total_sugars': 36.0, 'nutrition_protein': 5.5,
                'ingredients': 'Premium Dates, Full Cream Milk',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 54, 'name': 'Kesar Royal Milkshake', 'category': 'DRYFRUIT MILKSHAKES',
                'description': 'A regal, aromatic blend. Pure saffron (Kesar) infused into creamy milk for a soothing and luxurious experience.',
                'price': 150.00,
                'long_description': 'Inspired by royal traditions, this milkshake uses real saffron strands and a hint of cardamom. It is a soothing, golden-hued drink that is traditionally known to improve mood and provide a healthy glow.',
                'net_quantity_ml': 300,
                'features': ['Pure Saffron', 'Aromatic', 'Traditional Recipe', 'No Preservatives', 'Soothing'],
                'benefits': [
                    {'title': 'Mood Enhancer', 'description': 'Saffron is a natural mood lifter and helps reduce stress.'},
                    {'title': 'Skin Glow', 'description': 'Traditional remedy for promoting a natural, radiant complexion.'},
                    {'title': 'Better Sleep', 'description': 'Helps relax the nervous system for a restful night.'}
                ],
                'nutrition_calories': 170.00, 'nutrition_total_fat': 5.0, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 0.1, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 6.0,
                'ingredients': 'Pure Saffron Strands, Full Cream Milk, Cardamom',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 56, 'name': 'Kaju Anjeer Milkshake', 'category': 'DRYFRUIT MILKSHAKES',
                'description': 'A premium, thick blend of creamy Cashews and fiber-rich Figs (Anjeer). A luxurious shake that offers a perfect balance of crunch and sweetness.',
                'price': 150.00,
                'long_description': 'This shake is the ultimate energy-dense treat. We blend soaked figs with premium-grade cashews and fresh milk. The result is a naturally sweet, textured drink that is packed with minerals and healthy fats to keep you going all day.',
                'net_quantity_ml': 300,
                'features': ['Rich in Minerals', 'Premium Nuts', 'No Added Sugar', 'No Preservatives', 'Textured Blend'],
                'benefits': [
                    {'title': 'Stamina Builder', 'description': 'High calorie and nutrient density for physical strength.'},
                    {'title': 'Bone Health', 'description': 'Excellent source of calcium and magnesium for strong bones.'},
                    {'title': 'Gut Health', 'description': 'High fiber from figs supports healthy digestion.'}
                ],
                'nutrition_calories': 240.00, 'nutrition_total_fat': 10.5, 'nutrition_carbohydrate': 32.0,
                'nutrition_dietary_fiber': 3.8, 'nutrition_total_sugars': 24.0, 'nutrition_protein': 6.5,
                'ingredients': 'Premium Cashews, Dried Figs, Full Cream Milk',
                'allergen_info': 'Contains Milk, Contains Nuts (Cashews)'
            },
            {
                'id': 57, 'name': 'Kesar Badam Milkshake', 'category': 'DRYFRUIT MILKSHAKES',
                'description': 'A timeless Indian classic. Pure saffron (Kesar) and crushed almonds (Badam) blended into creamy milk for a royal and nourishing experience.',
                'price': 150.00,
                'long_description': 'Our Kesar Badam shake is made the traditional way. We use real saffron strands for color and aroma, combined with almonds that provide a subtle crunch and a boost of Vitamin E. It is a brain-boosting drink that is great for all ages.',
                'net_quantity_ml': 300,
                'features': ['Real Saffron', 'Crushed Almonds', 'Always Fresh', 'No Preservatives', 'Brain Food'],
                'benefits': [
                    {'title': 'Brain Power', 'description': 'Almonds are rich in riboflavin and L-carnitine for cognitive health.'},
                    {'title': 'Skin & Hair', 'description': 'High Vitamin E content promotes healthy skin and hair.'},
                    {'title': 'Immunity', 'description': 'Saffron and minerals help strengthen the body natural defenses.'}
                ],
                'nutrition_calories': 210.00, 'nutrition_total_fat': 9.2, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 2.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 7.2,
                'ingredients': 'Blanched Almonds, Saffron Strands, Full Cream Milk',
                'allergen_info': 'Contains Milk, Contains Nuts (Almonds)'
            },

            # KERALA SPECIALS AVIL MILKS (61-65)
            {
                'id': 61, 'name': 'Malabar Avil Milk', 'category': 'KERALA SPECIALS AVIL MILKS',
                'description': 'The authentic taste of Malabar. A unique layered drink featuring mashed bananas, roasted beaten rice (Avil), and chilled milk.',
                'price': 120.00,
                'long_description': 'Our Malabar Avil Milk is a traditional energy booster. We use perfectly ripe bananas mashed to a pulp, topped with crispy, golden-roasted beaten rice and peanuts for a delightful crunch in every sip. It is not just a drink; it is a snack in a glass.',
                'net_quantity_ml': 300,
                'features': ['Authentic Malabar Recipe', 'Crunchy Avil', 'Fresh Bananas', 'No Preservatives', 'Textured Drink'],
                'benefits': [
                    {'title': 'Instant Satiety', 'description': 'The combination of carbs and fiber makes it a very filling snack.'},
                    {'title': 'Natural Energy', 'description': 'Quick release energy from bananas and slow release from beaten rice.'},
                    {'title': 'Digestive Friendly', 'description': 'Avil (Beaten rice) is light on the stomach and easy to digest.'}
                ],
                'nutrition_calories': 220.00, 'nutrition_total_fat': 5.5, 'nutrition_carbohydrate': 38.0,
                'nutrition_dietary_fiber': 3.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 5.8,
                'ingredients': 'Roasted Beaten Rice (Avil), Fresh Bananas, Full Cream Milk, Roasted Peanuts',
                'allergen_info': 'Contains Milk, Contains Peanuts'
            },
            {
                'id': 62, 'name': 'Dry Fruit Avil Milk', 'category': 'KERALA SPECIALS AVIL MILKS',
                'description': 'A premium upgrade to the classic. The traditional Avil Milk enriched with a generous mix of chopped dates, cashews, and almonds.',
                'price': 140.00,
                'long_description': 'We have taken the classic Malabar Avil milk and made it Royal. Along with the crunch of roasted rice and peanuts, you get the richness of premium dry fruits, making it a nutrient-dense powerhouse.',
                'net_quantity_ml': 300,
                'features': ['Premium Dry Fruits', 'Crunchy Avil', 'No Added Sugar', 'No Preservatives', 'Iron Rich'],
                'benefits': [
                    {'title': 'Mineral Powerhouse', 'description': 'Packed with Iron, Magnesium, and Zinc from mixed dry fruits.'},
                    {'title': 'Brain Health', 'description': 'Nuts provide essential fatty acids for cognitive support.'},
                    {'title': 'High Stamina', 'description': 'A calorie-dense drink perfect for active individuals.'}
                ],
                'nutrition_calories': 280.00, 'nutrition_total_fat': 10.2, 'nutrition_carbohydrate': 42.0,
                'nutrition_dietary_fiber': 4.5, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 7.5,
                'ingredients': 'Beaten Rice, Bananas, Milk, Dates, Cashews, Almonds, Peanuts',
                'allergen_info': 'Contains Milk, Contains Nuts (Cashews, Almonds), Contains Peanuts'
            },
            {
                'id': 65, 'name': 'Special Avil Milk', 'category': 'KERALA SPECIALS AVIL MILKS',
                'description': 'Our signature creation. An extra-loaded version of Avil milk featuring a special blend of creams and a double serving of roasted crunch.',
                'price': 150.00,
                'long_description': 'Specially curated for those who love a richer, thicker Avil milk. We use a premium selection of bananas and a secret blend of milk creams to ensure this version is the most indulgent in our Kerala Special category.',
                'net_quantity_ml': 300,
                'features': ['Signature Blend', 'Double Crunch', 'Extra Creamy', 'No Preservatives', 'Premium Quality'],
                'benefits': [
                    {'title': 'Gourmet Experience', 'description': 'The ultimate treat for Avil milk enthusiasts.'},
                    {'title': 'Meal in a Bottle', 'description': 'Extremely filling and provides a complete macronutrient profile.'},
                    {'title': 'Mood Booster', 'description': 'The perfect sweet and crunchy treat to lift your spirits.'}
                ],
                'nutrition_calories': 265.00, 'nutrition_total_fat': 9.5, 'nutrition_carbohydrate': 40.0,
                'nutrition_dietary_fiber': 3.2, 'nutrition_total_sugars': 21.0, 'nutrition_protein': 6.5,
                'ingredients': 'Roasted Beaten Rice, Premium Bananas, Thickened Milk, Honey, Roasted Peanuts',
                'allergen_info': 'Contains Milk, Contains Peanuts'
            },

            # FALOODA (66)
            {
                'id': 66, 'name': 'Mumbai Special Falooda', 'category': 'FALOODA',
                'description': 'A legendary layered dessert drink. A beautiful symphony of rose syrup, silky vermicelli, cooling sabja seeds, and a scoop of ice cream.',
                'price': 160.00,
                'long_description': 'Inspired by the famous street-side Faloodas of Mumbai. This drink is a texture lover dream, featuring fragrant rose preserves, soft vermicelli (falooda sev), and basil seeds that act as a natural body coolant. It is finished with a scoop of premium vanilla ice cream for a rich, creamy end.',
                'net_quantity_ml': 300,
                'features': ['Layered Texture', 'Natural Coolant', 'Classic Recipe', 'No Preservatives', 'Dessert in a Glass'],
                'benefits': [
                    {'title': 'Naturally Cooling', 'description': 'Sabja (Basil) seeds are excellent for reducing body heat.'},
                    {'title': 'Digestive Support', 'description': 'Basil seeds are known to aid digestion and soothe the stomach.'},
                    {'title': 'Instant Mood Lifter', 'description': 'The aromatic rose and sweet cream provide a satisfying treat.'}
                ],
                'nutrition_calories': 210.00, 'nutrition_total_fat': 6.5, 'nutrition_carbohydrate': 34.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 28.0, 'nutrition_protein': 4.8,
                'ingredients': 'Milk, Rose Syrup, Vermicelli (Sev), Sabja Seeds, Ice Cream',
                'allergen_info': 'Contains Milk, Contains Gluten'
            },

            # THE MOJITO BAR (80-84)
            {
                'id': 80, 'name': 'Mint Mojito', 'category': 'THE MOJITO BAR',
                'description': 'The ultimate thirst quencher. A sparkling blend of fresh garden mint, zesty lime, and a touch of sweetness over crushed ice.',
                'price': 100.00,
                'long_description': 'Our Mint Mojito is the gold standard of refreshment. We muddle fresh mint leaves with lime wedges to release their natural oils, then top it off with sparkling soda. It is crisp, clean, and perfectly balanced to provide a cooling citrus kick.',
                'net_quantity_ml': 300,
                'features': ['Zero Alcohol', 'Freshly Muddled', 'Sparkling Refreshment', 'No Preservatives', 'Low Calorie'],
                'benefits': [
                    {'title': 'Digestive Relief', 'description': 'Fresh mint and lime aid in digestion and relieve bloating.'},
                    {'title': 'Instant Hydration', 'description': 'Perfect for replenishing fluids on a hot afternoon.'},
                    {'title': 'Breath Freshener', 'description': 'Natural mint provides a long-lasting clean feeling.'}
                ],
                'nutrition_calories': 85.00, 'nutrition_total_fat': 0.0, 'nutrition_carbohydrate': 21.0,
                'nutrition_dietary_fiber': 0.5, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 0.1,
                'ingredients': 'Fresh Mint, Fresh Lime, Sparkling Water, Cane Sugar',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 81, 'name': 'Blue Lagoon Mojito', 'category': 'THE MOJITO BAR',
                'description': 'Vibrant, cool, and tropical. A stunning blue-hued mojito with a refreshing citrus-orange profile.',
                'price': 100.00,
                'long_description': 'Dive into the deep blue with this visually striking drink. Combining the flavors of Curacao oranges with our signature lime and mint base, this mojito offers a slightly different citrus profile that is both sweet and tart.',
                'net_quantity_ml': 300,
                'features': ['Vibrant Color', 'Zero Alcohol', 'Citrus Twist', 'No Preservatives', 'Party Favorite'],
                'benefits': [
                    {'title': 'Refreshing Energy', 'description': 'The citrus blend provides a quick mental and physical pick-me-up.'},
                    {'title': 'Cooling Effect', 'description': 'The mint base helps in lowering perceived body temperature.'},
                    {'title': 'Low Calorie Treat', 'description': 'A light alternative to heavy milkshakes or sodas.'}
                ],
                'nutrition_calories': 90.00, 'nutrition_total_fat': 0.0, 'nutrition_carbohydrate': 23.0,
                'nutrition_dietary_fiber': 0.2, 'nutrition_total_sugars': 21.0, 'nutrition_protein': 0.1,
                'ingredients': 'Curacao Flavor, Fresh Lime, Mint, Sparkling Water',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 82, 'name': 'Watermelon Mojito', 'category': 'THE MOJITO BAR',
                'description': 'Summer in a bottle. Freshly crushed watermelon juice mixed with the classic mint and lime mojito base.',
                'price': 100.00,
                'long_description': 'We take the classic mojito and elevate it with the natural sweetness of watermelon. It is incredibly light, hydrating, and packed with lycopene, making it a guilt-free mojito that feels like a fruit juice with a sparkling twist.',
                'net_quantity_ml': 300,
                'features': ['Fruit Infused', 'Zero Alcohol', 'Lycopene Rich', 'No Preservatives', 'Always Fresh'],
                'benefits': [
                    {'title': 'Deep Hydration', 'description': 'Watermelon is 92% water, making this the perfect hydration drink.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Contains antioxidants that help reduce body inflammation.'},
                    {'title': 'Vitamin C Boost', 'description': 'Combined lime and watermelon provide a healthy dose of immunity vitamins.'}
                ],
                'nutrition_calories': 80.00, 'nutrition_total_fat': 0.1, 'nutrition_carbohydrate': 19.0,
                'nutrition_dietary_fiber': 0.4, 'nutrition_total_sugars': 17.0, 'nutrition_protein': 0.5,
                'ingredients': 'Fresh Watermelon, Lime, Mint, Sparkling Water',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 83, 'name': 'Green Apple Mojito', 'category': 'THE MOJITO BAR',
                'description': 'Tart, crisp, and energetic. A delicious blend of sour green apple flavors with refreshing lime and mint.',
                'price': 100.00,
                'long_description': 'For those who love a bit of zing. This mojito uses the sharp, acidic profile of green apple to create a drink that is more tart than sweet. It is highly invigorating and acts as a great palate cleanser.',
                'net_quantity_ml': 300,
                'features': ['Tart & Tangy', 'Zero Alcohol', 'Crisp Flavor', 'No Preservatives', 'Invigorating'],
                'benefits': [
                    {'title': 'Palate Cleanser', 'description': 'The acidity helps refresh the taste buds after a heavy meal.'},
                    {'title': 'Metabolic Spark', 'description': 'Natural fruit acids can help stimulate digestion.'},
                    {'title': 'Focus Boost', 'description': 'The sharp flavor profile provides a quick mental alert.'}
                ],
                'nutrition_calories': 95.00, 'nutrition_total_fat': 0.0, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 0.2, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 0.1,
                'ingredients': 'Green Apple Extract, Fresh Lime, Mint, Sparkling Water',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 84, 'name': 'Strawberry Mojito', 'category': 'THE MOJITO BAR',
                'description': 'A berry-infused sparkling delight. Freshly muddled strawberries blended with zesty lime and cooling mint.',
                'price': 100.00,
                'long_description': 'This mojito is a sweet and tart masterpiece. We use real strawberries to create a beautiful red hue and a natural berry flavor that complements the sharpness of the lime. It is a light, bubbly, and fruity alternative to classic sodas.',
                'net_quantity_ml': 300,
                'features': ['Real Fruit Base', 'Zero Alcohol', 'Antioxidant Rich', 'Sparkling', 'Refreshing'],
                'benefits': [
                    {'title': 'Skin Health', 'description': 'Strawberries are rich in Vitamin C and antioxidants for a healthy glow.'},
                    {'title': 'Low Calorie', 'description': 'A light and airy drink that satisfies sweet cravings without the weight.'},
                    {'title': 'Cooling', 'description': 'Mint and lime work together to soothe the digestive system.'}
                ],
                'nutrition_calories': 92.00, 'nutrition_total_fat': 0.1, 'nutrition_carbohydrate': 22.0,
                'nutrition_dietary_fiber': 0.6, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 0.3,
                'ingredients': 'Fresh Strawberries, Lime, Mint, Sparkling Water',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },

            # ICE CREAM MILK SHAKE (102-105)
            {
                'id': 102, 'name': 'Oreo Milk Shake', 'category': 'ICE CREAM MILK SHAKE',
                'description': 'The ultimate cookie-lover dream. A thick, creamy shake loaded with crunchy Oreo cookie bits and premium vanilla ice cream.',
                'price': 110.00,
                'long_description': 'Our Oreo Milk Shake is a decadent treat. We blend real Oreo cookies into a base of rich, full-cream milk and velvety ice cream. Every sip offers a perfect balance of smooth cream and chocolatey cookie crunch.',
                'net_quantity_ml': 300,
                'features': ['Crunchy Bits', 'Thick & Creamy', 'Real Oreo Cookies', 'No Preservatives', 'Indulgent Dessert'],
                'benefits': [
                    {'title': 'Fun Texture', 'description': 'A delightful mix of smooth cream and crunchy cookie pieces.'},
                    {'title': 'Instant Happiness', 'description': 'A classic comfort drink that acts as a great mood booster.'},
                    {'title': 'High Energy', 'description': 'Provides a quick carbohydrate boost for an afternoon pick-me-up.'}
                ],
                'nutrition_calories': 245.00, 'nutrition_total_fat': 10.5, 'nutrition_carbohydrate': 34.0,
                'nutrition_dietary_fiber': 0.8, 'nutrition_total_sugars': 26.0, 'nutrition_protein': 5.0,
                'ingredients': 'Oreo Biscuits, Premium Ice Cream, Full Cream Milk',
                'allergen_info': 'Contains Milk, Contains Gluten, Contains Soya'
            },
            {
                'id': 103, 'name': 'KitKat Shake', 'category': 'ICE CREAM MILK SHAKE',
                'description': 'A chocolate-wafer sensation. Creamy milkshake blended with crushed KitKat bars for a unique crispy-creamy texture.',
                'price': 110.00,
                'long_description': 'Take a break with our KitKat Shake. We blend crispy wafer chocolate bars with chilled milk and ice cream. It features a distinct malted chocolate flavor and small wafer pieces that provide a satisfying crunch.',
                'net_quantity_ml': 300,
                'features': ['Chocolate Wafer Crunch', 'Thickened Base', 'Real KitKat', 'No Preservatives', 'Creamy Finish'],
                'benefits': [
                    {'title': 'Textural Variety', 'description': 'Offers a unique mouthfeel with crispy wafer layers and smooth milk.'},
                    {'title': 'Sweet Indulgence', 'description': 'The perfect treat for chocolate and wafer enthusiasts.'},
                    {'title': 'Satisfying Treat', 'description': 'Heavy enough to serve as a filling dessert or snack.'}
                ],
                'nutrition_calories': 255.00, 'nutrition_total_fat': 11.2, 'nutrition_carbohydrate': 32.0,
                'nutrition_dietary_fiber': 0.5, 'nutrition_total_sugars': 24.0, 'nutrition_protein': 4.8,
                'ingredients': 'KitKat Chocolate, Premium Ice Cream, Full Cream Milk',
                'allergen_info': 'Contains Milk, Contains Gluten, Contains Soya'
            },
            {
                'id': 104, 'name': 'Snickers Shake', 'category': 'ICE CREAM MILK SHAKE',
                'description': 'A nutty, chocolatey, and caramel-infused shake. Blended with real Snickers for a powerful protein-packed flavor.',
                'price': 110.00,
                'long_description': 'For those who love the combination of nuts and chocolate. This shake features the iconic flavors of roasted peanuts, caramel, and nougat blended into a thick ice cream shake. It is salty, sweet, and incredibly rich.',
                'net_quantity_ml': 300,
                'features': ['Nutty & Salty', 'Caramel Infused', 'Real Snickers', 'No Preservatives', 'High Satiety'],
                'benefits': [
                    {'title': 'Protein Boost', 'description': 'Peanuts in the bar provide a small boost of plant-based protein.'},
                    {'title': 'Flavor Balance', 'description': 'The perfect mix of sweet caramel and salty nuts.'},
                    {'title': 'Extremely Filling', 'description': 'One of our most calorie-dense and satisfying shakes.'}
                ],
                'nutrition_calories': 275.00, 'nutrition_total_fat': 13.5, 'nutrition_carbohydrate': 30.0,
                'nutrition_dietary_fiber': 1.2, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 6.5,
                'ingredients': 'Snickers Bar, Premium Ice Cream, Full Cream Milk, Peanuts',
                'allergen_info': 'Contains Milk, Contains Peanuts, Contains Soya'
            },
            {
                'id': 105, 'name': 'Belgian Chocolate Shake', 'category': 'ICE CREAM MILK SHAKE',
                'description': 'Deep, dark, and sophisticated. A rich milkshake made with premium Belgian-style cocoa for the ultimate chocolate experience.',
                'price': 140.00,
                'long_description': 'This is not your average chocolate milk. We use a high-quality, dark Belgian cocoa powder and dark chocolate chips blended with creamy vanilla ice cream. It is intense, slightly bitter, and perfectly sweet—a true chocolate lover delight.',
                'net_quantity_ml': 300,
                'features': ['Gourmet Cocoa', 'Dark Chocolate', 'Silky Smooth', 'No Preservatives', 'Premium Quality'],
                'benefits': [
                    {'title': 'Antioxidant Rich', 'description': 'Dark cocoa is packed with flavonoids that support heart health.'},
                    {'title': 'Mood Enhancer', 'description': 'Chocolate triggers the release of endorphins for a happy feeling.'},
                    {'title': 'Rich Flavor Profile', 'description': 'A more mature and intense chocolate taste compared to standard shakes.'}
                ],
                'nutrition_calories': 230.00, 'nutrition_total_fat': 9.8, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 2.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 5.5,
                'ingredients': 'Dark Belgian Cocoa, Chocolate Chips, Premium Ice Cream, Full Cream Milk',
                'allergen_info': 'Contains Milk, Contains Soya'
            },

            # CREAMY FRUIT DELIGHT (111-112)
            {
                'id': 111, 'name': 'Mango Cream', 'category': 'CREAMY FRUIT DELIGHT',
                'description': 'Pure indulgence in a glass. Layers of thick fresh cream topped with hand-cut chunks of sweet, seasonal mangoes.',
                'price': 150.00,
                'long_description': 'Inspired by the famous desserts of Mahabaleshwar, our Mango Cream is a luxury treat. We use whipped heavy cream and blend it with a fresh mango puree, finishing it with generous pieces of Alphonso or seasonal mangoes. No artificial flavors, just pure fruit and dairy.',
                'net_quantity_ml': 300,
                'features': ['Fresh Fruit Chunks', 'Heavy Cream', 'Seasonal Favorite', 'No Preservatives', 'Gourmet Dessert'],
                'benefits': [
                    {'title': 'Rich in Vitamin A', 'description': 'Mangoes provide essential nutrients for eye health and immunity.'},
                    {'title': 'High Energy', 'description': 'The combination of healthy fats and fruit sugars provides a satisfying energy boost.'},
                    {'title': 'Natural Sweetness', 'description': 'Relies on the natural sugar of ripe mangoes.'}
                ],
                'nutrition_calories': 280.00, 'nutrition_total_fat': 18.0, 'nutrition_carbohydrate': 28.0,
                'nutrition_dietary_fiber': 1.5, 'nutrition_total_sugars': 22.0, 'nutrition_protein': 3.5,
                'ingredients': 'Fresh Mango Chunks, Fresh Heavy Cream, Alphonso Puree',
                'allergen_info': 'Contains Milk'
            },
            {
                'id': 112, 'name': 'Strawberry Cream', 'category': 'CREAMY FRUIT DELIGHT',
                'description': 'A classic berry delight. Luscious fresh cream paired with sliced garden-fresh strawberries for a perfect sweet-tart balance.',
                'price': 150.00,
                'long_description': 'Our Strawberry Cream features layers of velvety whipped cream and macerated strawberries. The natural acidity of the berries cuts through the richness of the cream, creating a light yet indulgent dessert that is a global favorite.',
                'net_quantity_ml': 300,
                'features': ['Real Strawberries', 'No Syrups', 'Whipped Cream', 'No Preservatives', 'Handcrafted'],
                'benefits': [
                    {'title': 'Antioxidant Rich', 'description': 'Strawberries are packed with polyphenols that protect the heart.'},
                    {'title': 'Skin Support', 'description': 'High Vitamin C content helps in collagen synthesis.'},
                    {'title': 'Satisfying Satiety', 'description': 'The healthy fats in cream keep you full and satisfied.'}
                ],
                'nutrition_calories': 260.00, 'nutrition_total_fat': 17.0, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 2.0, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 3.2,
                'ingredients': 'Fresh Strawberries, Fresh Heavy Cream, Hint of Honey',
                'allergen_info': 'Contains Milk'
            },

            # FRUITS & SCOOPS (118)
            {
                'id': 118, 'name': 'Fruit Salad with Ice Cream', 'category': 'FRUITS & SCOOPS',
                'description': 'The best of both worlds. A medley of chilled seasonal fruits served with a generous scoop of premium vanilla ice cream.',
                'price': 150.00,
                'long_description': 'A nostalgic treat that combines health and indulgence. We take our fresh fruit medley—including papaya, apple, and pineapple—and top it with a velvety scoop of ice cream. The melting cream acts as a natural sauce for the fresh fruit.',
                'net_quantity_ml': 300,
                'features': ['Fresh Fruit Medley', 'Premium Ice Cream', 'No Preservatives', 'Dual Texture', 'Hydrating & Sweet'],
                'benefits': [
                    {'title': 'Fiber & Calcium', 'description': 'Get the digestive benefits of whole fruits with the calcium of dairy.'},
                    {'title': 'Cooling Dessert', 'description': 'Perfect for lowering body temperature and satisfying a sweet tooth.'},
                    {'title': 'Natural Vitamins', 'description': 'A diverse range of vitamins from multiple fruit sources.'}
                ],
                'nutrition_calories': 190.00, 'nutrition_total_fat': 6.0, 'nutrition_carbohydrate': 32.0,
                'nutrition_dietary_fiber': 3.5, 'nutrition_total_sugars': 26.0, 'nutrition_protein': 3.8,
                'ingredients': 'Apple, Papaya, Pineapple, Watermelon, Vanilla Ice Cream',
                'allergen_info': 'Contains Milk'
            },

            # FRUIT BOWLS (121, 123)
            {
                'id': 121, 'name': 'Mix Fruit Bowl', 'category': 'FRUIT BOWLS',
                'description': '100% whole fresh seasonal fruits. A clean, colorful, and fiber-rich bowl for the ultimate healthy snack.',
                'price': 120.00,
                'long_description': 'Our Mix Fruit Bowl is the purest way to enjoy nature candy. We use bite-sized pieces of the freshest seasonal produce, typically including apple, papaya, watermelon, and pineapple. No added sugar, dressing, or salt—just pure fruit.',
                'net_quantity_ml': 300,
                'features': ['Whole Fruit', 'No Added Sugar', 'Fiber Rich', 'Zero Fat', 'Always Fresh'],
                'benefits': [
                    {'title': 'Natural Cleanse', 'description': 'High fiber and water content help detoxify the digestive tract.'},
                    {'title': 'Immune Support', 'description': 'A wide spectrum of vitamins from different fruit groups.'},
                    {'title': 'Weight Management', 'description': 'Low in calories but high in volume to keep you full.'}
                ],
                'nutrition_calories': 95.00, 'nutrition_total_fat': 0.3, 'nutrition_carbohydrate': 24.0,
                'nutrition_dietary_fiber': 4.5, 'nutrition_total_sugars': 18.0, 'nutrition_protein': 1.2,
                'ingredients': 'Seasonal Apple, Papaya, Watermelon, Pineapple',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
            {
                'id': 123, 'name': 'Papaya Bowl', 'category': 'FRUIT BOWLS',
                'description': 'Freshly diced cubes of ripe, sweet papaya. A simple, effective, and nutrient-dense bowl for digestive health.',
                'price': 80.00,
                'long_description': 'Our Papaya Bowl features premium, hand-picked papayas. Known as the angel of fruits, this bowl is specifically prepared to be a light, refreshing meal that supports gut health and provides a massive dose of Vitamin A.',
                'net_quantity_ml': 300,
                'features': ['Mono-Fruit Bowl', 'Digestive Enzyme Rich', 'High Vitamin A', 'No Added Sugar', 'Always Fresh'],
                'benefits': [
                    {'title': 'Gut Health', 'description': 'Rich in papain to help break down proteins and ease bloating.'},
                    {'title': 'Vision & Skin', 'description': 'High Beta-carotene levels support eyes and glowing skin.'},
                    {'title': 'Anti-Inflammatory', 'description': 'Helps in reducing internal inflammation and supports recovery.'}
                ],
                'nutrition_calories': 105.00, 'nutrition_total_fat': 0.2, 'nutrition_carbohydrate': 26.0,
                'nutrition_dietary_fiber': 4.2, 'nutrition_total_sugars': 19.0, 'nutrition_protein': 1.1,
                'ingredients': 'Fresh Ripe Papaya',
                'allergen_info': 'No Mustard, No Nuts, No Peanuts, No Sesame, No Soya, No Milk'
            },
        ]

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting comprehensive product seed...')
        
        products_data = self.get_all_products()
        created_count = 0
        updated_count = 0
        
        for product in products_data:
            category_name = product.pop('category')
            
            # Get or create category
            category, _ = Category.objects.get_or_create(name=category_name)
            
            # Prepare product data
            product['category'] = category
            product['price'] = Decimal(str(product['price']))
            product['is_active'] = True
            
            # Create or update juice
            juice, created = Juice.objects.update_or_create(
                id=product['id'],
                defaults=product
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'CREATED: {juice.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'UPDATED: {juice.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nComplete! Created: {created_count}, Updated: {updated_count}'))
