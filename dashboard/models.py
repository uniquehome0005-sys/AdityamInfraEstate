from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    # Account type
    is_agent = models.BooleanField(default=False)

    # Profile Images
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    poster = models.ImageField(upload_to='users/posters/', blank=True, null=True)

    # Agent Information
    description = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # Social Media
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

class PropertyType(models.Model):
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ]

    PREFERENCE_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent / Lease'),
        ('pg', 'PG'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    preference = models.CharField(
        max_length=50,
        choices=PREFERENCE_CHOICES,
        blank=True,
        null=True,
        help_text="Optional: if set, this type is only for this preference"
    )

    def __str__(self):
        return f"{self.name} ({self.category}-{self.preference})"


class Property(models.Model):

    LABEL_CHOICES = (
        ('new', 'New Listing'),
        ('open', 'Open House'),
    )

    AVAILABILITY_CHOICES = (
        ('rtm', 'Ready to Move'),
        ('construction', 'Under Construction'),
    )

    OWNERSHIP_CHOICES = (
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('cooperative', 'Co-operative'),
        ('poa', 'Power of Attorney'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Address
    house_no = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255)
    locality = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default="Jaipur")
    state = models.CharField(max_length=100, default="Rajasthan")
    country = models.CharField(max_length=100, default="India")
    zipcode = models.CharField(max_length=10)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    before_price_label = models.CharField(max_length=50, blank=True)
    after_price_label = models.CharField(max_length=50, blank=True)

    # Property Details
    property_label = models.CharField(max_length=10, choices=LABEL_CHOICES)
    property_types = models.ForeignKey(PropertyType, related_name="types", on_delete=models.CASCADE)

    # Area
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    carpet_area = models.FloatField(null=True, blank=True)
    builtup_area = models.FloatField(null=True, blank=True)
    super_area = models.FloatField(null=True, blank=True)
    carpet_area_unit = models.CharField(max_length=20, default="sqft")
    builtup_area_unit = models.CharField(max_length=20, null=True, blank=True)
    super_area_unit = models.CharField(max_length=20, null=True, blank=True)

    # Rooms
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    balconies = models.PositiveIntegerField(default=0)

    # Floor
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    property_on_floor = models.CharField(max_length=10, blank=True)

    # Other
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='rtm')
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES, default='freehold')

    # Media
    video_url = models.URLField(blank=True)
    virtual_tour_code = models.TextField(blank=True)
    video_type = models.CharField(max_length=10, default="auto")
    video_file = models.FileField(upload_to="property_videos/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="properties/images/")

class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

class FloorPlan(models.Model):
    property = models.ForeignKey(Property, related_name="floors", on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_postfix = models.CharField(max_length=20, blank=True)

    size = models.PositiveIntegerField()
    size_postfix = models.CharField(max_length=20, blank=True)

    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()

    image = models.ImageField(upload_to="properties/floors/")
    description = models.TextField(blank=True)

class PropertyNearby(models.Model):
    property = models.ForeignKey(
        Property,
        related_name="nearby_places",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)   # School, Hospital, Metro, etc.
    distance_km = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.name} - {self.distance_km} km"


class ExploreCities(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="locations/")
    property_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BenefitSection(models.Model):
    subtitle = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="benefits/")

    def __str__(self):
        return self.title


class Benefit(models.Model):
    section = models.ForeignKey(
        BenefitSection,
        related_name="benefits",
        on_delete=models.CASCADE
    )
    icon_class = models.CharField(
        max_length=50,
        help_text="Example: icon-proven, icon-customize"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="testimonials"
    )

    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def stars(self):
        return range(self.rating)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class FAQPage(models.Model):
    title = models.CharField(
        max_length=200,
        default="Frequently Asked Questions"
    )
    background_image = models.ImageField(
        upload_to="faq_page/",
        blank=True,
        null=True
    )

    def __str__(self):
        return "FAQ Page Settings"

    def save(self, *args, **kwargs):
        # Allow only ONE instance
        if not self.pk and FAQPage.objects.exists():
            raise ValueError("Only one FAQ Page instance allowed.")
        return super().save(*args, **kwargs)


class FAQ(models.Model):

    CATEGORY_CHOICES = [
        ("overview", "Overview"),
        ("costs", "Costs and Payments"),
        ("safety", "Safety and Security"),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="overview"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return self.question


class Agent(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrative Staff'),
        ('agent', 'Real Estate Agent'),
        ('manager', 'Manager'),
    ]

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='agents/')
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_visble = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactPage(models.Model):
    title = models.CharField(max_length=200, default="Contact Us")
    background_image = models.ImageField(upload_to="contact_page/", blank=True, null=True)

    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    open_time = models.TextField()

    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Contact Page Settings"

    def save(self, *args, **kwargs):
        if not self.pk and ContactPage.objects.exists():
            raise ValueError("Only one Contact Page instance allowed.")
        return super().save(*args, **kwargs)

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class PricingPage(models.Model):
    title = models.CharField(
        max_length=200,
        default="Pricing"
    )
    subTitle = models.CharField(
        max_length=200,
        default="Our Subscription"
    )
    background_image = models.ImageField(
        upload_to="pricing/",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Pricing Settings"

    def save(self, *args, **kwargs):
        if not self.pk and PricingPage.objects.exists():
            raise ValueError("Only one Pricing Page instance allowed.")
        return super().save(*args, **kwargs)


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_period = models.CharField(max_length=50, default="month")
    description = models.TextField()
    button_text = models.CharField(max_length=100, default="View All Properties")
    button_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name='features'
    )
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.plan.name} - {self.title}"


class ServicePage(models.Model):
    title = models.CharField(
        max_length=200,
        default="Our Services"
    )
    subTitle = models.CharField(
        max_length=200,
        default="Our Location For You"
    )
    background_image = models.ImageField(
        upload_to="service/",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Service Settings"

    def save(self, *args, **kwargs):
        if not self.pk and ServicePage.objects.exists():
            raise ValueError("Only one Service Page instance allowed.")
        return super().save(*args, **kwargs)

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="service/",
        blank=True,
        null=True
    )
    link_url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# Create your models here.
