from django.db import models

# Create your models here.

class Restaurant(models.Model):
    #fields are restaurant_name, description, location, address_1, address_2, street, city, total_seats, x1_tables, x2_tables, x4_tables, x6_tables, x10_communal, is_veg, menu_items, has_bar, has_private_dining, has_catering, promo_scheme, scheme_start_date, scheme_end_date, promo_credits, service_start_time, service_end_time, off_days, emergency_stop, is_active, is_deleted
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    x1_tables = models.IntegerField()
    x2_tables = models.IntegerField()
    x4_tables = models.IntegerField()
    x6_tables = models.IntegerField()
    x10_communal = models.IntegerField()
    is_veg = models.BooleanField()
    has_bar = models.BooleanField()
    has_private_dining = models.BooleanField()
    has_catering = models.BooleanField()
    # promo_scheme = models.CharField(max_length=100) -> foreign > Schemes
    # promo_scheme = models.TextField() -> foreign > PromoScheme
    scheme_start_date = models.DateField()
    scheme_end_date = models.DateField()
    promo_credits = models.IntegerField()
    service_start_time = models.TimeField()
    service_end_time = models.TimeField()
    # off_days = models.TextField() -> foreign -> weekdays
    emergency_stop = models.BooleanField()
    is_active = models.BooleanField()
    is_deleted = models.BooleanField()

    def __str__(self):
        return self.name

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')
    
    def __str__(self):
        return self.restaurant.name
    
class MenuItem(models.Model):
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name
    
class ItemDetail(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items_of_restaurant')
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    is_veg = models.BooleanField()

    def __str__(self):
        return self.menu_items.item_name
    
class ItemImage(models.Model):
    item_details = models.ForeignKey(ItemDetail, on_delete=models.CASCADE, related_name='images_of_item')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return self.image

    # Menu timing model

class MenuTime(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def timing_validation(self):
        if self.from_time >= self.to_time:
            raise ValueError("From time cannot be greater than or equal to to time")
        else:
            return True

    # Breakfast menu Timing and items

class DiningMenu(models.Model):
    menu_type = models.CharField(max_length=100, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('specials', 'Specials'),
    ])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_menu')
    hours = models.ForeignKey(MenuTime, on_delete=models.CASCADE)
    menu_item = models.ManyToManyField(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu_type} menu of {self.restaurant.name} Restaurant"
    

    
class ItemDetailForCatering(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='catering_menu_items_of_restaurant')
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    is_veg = models.BooleanField()

class CateringMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='catering_menu')
    items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    service_cost_per_diner = models.FloatField()
    cutlery_cost_per_diner = models.FloatField()
    glassware_cost_per_diner = models.FloatField()
    menu_items = models.ManyToManyField(ItemDetailForCatering)
