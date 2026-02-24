from django.utils.html import format_html
from django.contrib import admin
from .models import (
    Property,
    PropertyImage,
    Amenity,
    PropertyAmenity,
    FloorPlan,
    PropertyNearby,
    ExploreCities,
    Benefit,
    BenefitSection,
    Testimonial,
    FAQPage,
    FAQ,
    Agent,
    ContactPage,
    ContactMessage,
    PricingPlan,
    PlanFeature,
    PricingPage,
    ServicePage,
    Service,
)


# ----------------------------------
# Inline Admins
# ----------------------------------

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1

class PropertyNearbyInline(admin.TabularInline):
    model = PropertyNearby
    extra = 1

# ----------------------------------
# Property Admin
# ----------------------------------

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "property_id",
        "property_type",
        "property_status",
        "price",
        "user",
        "created_at",
    )

    list_filter = (
        "property_type",
        "property_status",
        "property_label",
        "country",
        "state",
        "created_at",
    )

    search_fields = (
        "title",
        "property_id",
        "address",
        "zipcode",
        "neighborhood",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    inlines = [
        PropertyImageInline,
        PropertyAmenityInline,
        FloorPlanInline,
        PropertyNearbyInline,  # ✅ ADDED
    ]

    fieldsets = (
        ("Owner", {
            "fields": ("user",)
        }),

        ("Basic Information", {
            "fields": ("title", "description")
        }),

        ("Location", {
            "fields": (
                "address",
                "neighborhood",
                "state",
                "country",
                "zipcode",
                ("latitude", "longitude"),
            )
        }),

        ("Pricing", {
            "fields": (
                "price",
                "unit_price",
                ("before_price_label", "after_price_label"),
            )
        }),

        ("Property Details", {
            "fields": (
                ("property_type", "property_status", "property_label"),
                ("size_sqft", "land_area_sqft"),
                "property_id",
                ("rooms", "bedrooms", "bathrooms"),
                ("garages", "garage_size_sqft"),
                "year_built",
            )
        }),

        ("Media", {
            "fields": (
                "video_url",
                "virtual_tour_code",
            )
        }),

        ("System Info", {
            "fields": ("created_at",),
        }),
    )


# ----------------------------------
# Amenity Admin
# ----------------------------------

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ----------------------------------
# Property Image Admin
# ----------------------------------

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property", "image")


# ----------------------------------
# Property Amenity Admin
# ----------------------------------

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ("property", "amenity")
    list_filter = ("amenity",)


# ----------------------------------
# Floor Plan Admin
# ----------------------------------

@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "name",
        "size",
        "bedrooms",
        "bathrooms",
    )
    search_fields = ("name", "property__title")


@admin.register(PropertyNearby)
class PropertyNearbyAdmin(admin.ModelAdmin):
    list_display = ("property", "name", "distance_km")
    list_filter = ("name",)
    search_fields = ("name", "property__title")


@admin.register(ExploreCities)
class ExploreCitiesAdmin(admin.ModelAdmin):
    list_display = ("name", "property_count", "slug", "image_preview")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("name",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1


@admin.register(BenefitSection)
class BenefitSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview")
    inlines = [BenefitInline]
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 120px; height: auto; border-radius: 8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "is_active", "created_at")
    list_filter = ("rating", "is_active")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(FAQPage)
class FAQPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not FAQPage.objects.exists()


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    ordering = ('category', 'order')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'role',
        'phone',
        'email',
        'is_active',
        'created_at',
    )

    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('is_active',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'photo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Social Media Links', {
            'fields': ('facebook', 'twitter', 'linkedin', 'instagram')
        }),
        ('Status', {
            'fields': ('is_active', 'is_visble',)
        }),
    )


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        if ContactPage.objects.exists():
            return False
        return True


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'subject',
        'created_at',
        'is_read',
    )

    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(PricingPage)
class PricingPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        if PricingPage.objects.exists():
            return False
        return True

class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    fields = ('title', 'is_active')
    ordering = ('id',)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_period')
    search_fields = ('name',)
    list_filter = ('billing_period',)
    inlines = [PlanFeatureInline]


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan', 'is_active')
    list_filter = ('is_active', 'plan')
    search_fields = ('title',)


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        if ServicePage.objects.exists():
            return False
        return True


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_url', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')
    search_fields = ('title', 'description')
    ordering = ('order',)
