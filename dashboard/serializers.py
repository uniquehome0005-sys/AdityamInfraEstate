from rest_framework import serializers

from dashboard.utils import generate_property_video
from .models import Property, PropertyAmenity, PropertyType, Amenity, PropertyImage, FloorPlan
from django.core.files import File
import json, os

class PropertySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            video_type = request.data.get("video_type")

            property_obj = Property.objects.create(**validated_data)

            images = request.FILES.getlist("images")

            for img in images:
                PropertyImage.objects.create(property=property_obj, image=img)

            amenities = request.data.getlist("amenities")

            for amenity_id in amenities:
                PropertyAmenity.objects.create(
                    property=property_obj,
                    amenity_id=amenity_id
                )

            floor_plans = request.data.get("floor_plans")

            if floor_plans:
                floor_plans = json.loads(floor_plans)
                floor_images = request.FILES.getlist("floor_image")

                for index, floor in enumerate(floor_plans):
                    image = floor_images[index] if index < len(floor_images) else None

                    FloorPlan.objects.create(
                        property=property_obj,
                        name=floor.get("name"),
                        price=floor.get("price") or 0,
                        price_postfix=floor.get("price_postfix", ""),
                        size=floor.get("size") or 0,
                        size_postfix=floor.get("size_postfix", ""),
                        bedrooms=floor.get("bedrooms") or 0,
                        bathrooms=floor.get("bathrooms") or 0,
                        description=floor.get("description", ""),
                        image=image
                    )

            if video_type == "auto":

                images_qs = PropertyImage.objects.filter(property=property_obj)
                image_paths = [img.image.path for img in images_qs]

                if image_paths:
                    video_path = generate_property_video(image_paths)

                    with open(video_path, "rb") as f:
                        property_obj.video_file.save(
                            f"property_{property_obj.id}.mp4",
                            File(f),
                            save=True
                        )

                    os.remove(video_path)

            else:
                video_file = request.FILES.get("video_file")

                if video_file:
                    property_obj.video_file = video_file
                    property_obj.save()

            return property_obj

        except Exception as e:
            print("ERROR:", e)
            raise e   # IMPORTANT: don't hide error