from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Branch(models.Model):
    """Store branch/location information"""
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        verbose_name_plural = "Branches"
        ordering = ['city', 'name']


class BranchProduct(models.Model):
    """Link table for branch-specific product availability"""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_products')
    product = models.ForeignKey('Juice', on_delete=models.CASCADE, related_name='branch_availability')
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['branch', 'product']
        verbose_name = "Branch Product Availability"
        verbose_name_plural = "Branch Product Availability"
        ordering = ['branch', 'product']
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.product.name} at {self.branch.name} - {status}"


class Juice(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='juices'
    )
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='juices/')
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Extended product information
    long_description = models.TextField(
        blank=True,
        help_text="Detailed product description for detail page"
    )
    
    # Fixed quantity (always 250ml)
    net_quantity_ml = models.IntegerField(
        default=300,
        help_text="Net quantity in ml (fixed at 300ml)"
    )
    
    # Features (stored as JSON list)
    features = models.JSONField(
        default=list,
        blank=True,
        help_text='List of feature tags like ["All Natural", "No Preservatives", "Always Fresh"]'
    )
    
    # Benefits (stored as JSON list of objects with title and description)
    benefits = models.JSONField(
        default=list,
        blank=True,
        help_text='List of benefits with title and description: [{"title": "Immunity Booster", "description": "Packed with Vitamin C..."}]'
    )
    
    # Nutritional Information (per 200ml serving)
    nutrition_calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Calories per 200ml"
    )
    nutrition_total_fat = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total fat in grams"
    )
    nutrition_carbohydrate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Carbohydrate in grams"
    )
    nutrition_dietary_fiber = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dietary fiber in grams"
    )
    nutrition_total_sugars = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total sugars in grams"
    )
    nutrition_protein = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Protein in grams"
    )
    
    # Ingredients
    ingredients = models.TextField(
        blank=True,
        help_text="Main ingredients (e.g., 'Fresh Mandarin')"
    )
    
    # Allergen Information
    allergen_info = models.TextField(
        blank=True,
        help_text="Allergen warnings (e.g., 'No Mustard, No Nuts, No Peanuts')"
    )

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

