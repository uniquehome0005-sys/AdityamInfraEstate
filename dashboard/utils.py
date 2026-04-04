from dashboard.models import Property, PropertyAmenity
from django.utils.crypto import get_random_string
from django.core.files.base import ContentFile
from copy import deepcopy
import os

def duplicate_property():
    original = Property.objects.last()

    new_property = deepcopy(original)
    new_property.pk = None
    new_property.property_id = get_random_string(8)
    new_property.save()

    for img in original.images.all():
        img.pk = None
        img.property = new_property

        if img.image:
            img.image.open()
            img.image = ContentFile(
                img.image.read(),
                name=os.path.basename(img.image.name)
            )

        img.save()

    for floor in original.floors.all():
        floor.pk = None
        floor.property = new_property

        if floor.image:
            floor.image.open()
            floor.image = ContentFile(
                floor.image.read(),
                name=os.path.basename(floor.image.name)
            )

        floor.save()

    for pa in PropertyAmenity.objects.filter(property=original):
        PropertyAmenity.objects.create(
            property=new_property,
            amenity=pa.amenity
        )

    for nearby in original.nearby_places.all():
        nearby.pk = None
        nearby.property = new_property
        nearby.save()

    return new_property


# Create your views here.
