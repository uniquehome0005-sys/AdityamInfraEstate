import random
from django.core.management.base import BaseCommand
from django.core.files import File
# from django.contrib.auth.models import User
from faker import Faker

from ...models import (
    Property,
    PropertyImage,
    Amenity,
    PropertyAmenity,
    FloorPlan,
    PropertyNearby,
)

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake properties (50 listings)"

    def handle(self, *args, **kwargs):
        # user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("❌ Please create at least one user first"))
            return

        # ---------- AMENITIES ----------
        amenity_names = [
            "Swimming Pool",
            "Gym",
            "Parking",
            "WiFi",
            "Garden",
            "Security",
            "Elevator",
        ]

        amenities = []
        for name in amenity_names:
            amenity, _ = Amenity.objects.get_or_create(name=name)
            amenities.append(amenity)

        # ---------- IMAGES ----------
        property_images = [
            "media/properties/images/banner-property-1.jpg",
            "media/properties/images/banner-property-2.jpg",
            "media/properties/images/banner-property-3.jpg",
        ]

        floor_image = "media/properties/floors/floor1.png"

        # ---------- CREATE 50 PROPERTIES ----------
        for i in range(50):
            property_obj = Property.objects.create(
                user=user,
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                address=fake.address(),
                zipcode=fake.postcode(),
                country="USA",
                state=fake.state(),
                neighborhood=fake.city(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                price=random.randint(100000, 950000),
                unit_price=random.randint(100, 800),
                before_price_label="From",
                after_price_label="USD",
                property_type=random.choice(
                    ["apartment", "villa", "studio", "office", "townhouse"]
                ),
                property_status=random.choice(["rent", "sale"]),
                property_label=random.choice(["new", "open"]),
                size_sqft=random.randint(600, 4000),
                land_area_sqft=random.randint(1000, 8000),
                property_id=f"PROP-{fake.unique.random_int(10000, 99999)}",
                rooms=random.randint(2, 8),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 4),
                garages=random.randint(0, 3),
                garage_size_sqft=random.randint(200, 600),
                year_built=random.randint(1995, 2024),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                virtual_tour_code="<iframe></iframe>",
            )

            # ---------- PROPERTY IMAGES ----------
            for idx, img_path in enumerate(property_images):
                with open(img_path, "rb") as img:
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=File(
                            img,
                            name=f"property_{property_obj.id}_{idx}.jpg",
                        ),
                    )

            # ---------- AMENITIES ----------
            for amenity in random.sample(amenities, k=random.randint(3, 5)):
                PropertyAmenity.objects.create(
                    property=property_obj,
                    amenity=amenity,
                )

            # ---------- FLOOR PLAN ----------
            with open(floor_image, "rb") as img:
                FloorPlan.objects.create(
                    property=property_obj,
                    name="Main Floor Plan",
                    price=random.randint(80000, 300000),
                    price_postfix="Starting",
                    size=random.randint(500, 2000),
                    size_postfix="sqft",
                    bedrooms=random.randint(1, 4),
                    bathrooms=random.randint(1, 3),
                    image=File(img, name=f"floor_{property_obj.id}.jpg"),
                    description=fake.text(),
                )

            # ---------- NEARBY PLACES ----------
            nearby_places = ["School", "Hospital", "Mall", "Metro Station", "Park"]

            for place in random.sample(nearby_places, k=3):
                PropertyNearby.objects.create(
                    property=property_obj,
                    name=place,
                    distance_km=round(random.uniform(0.5, 5.0), 2),
                )

        self.stdout.write(
            self.style.SUCCESS("✅ Successfully created 50 fake properties!")
        )
