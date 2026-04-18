from django.views.generic import TemplateView
from django.views.generic import DetailView, FormView
from django.contrib.auth import authenticate, login
from dashboard.forms import ContactMessageForm
# from dashboard.data import duplicate_property
from .models import (
    Property, 
    PropertyAmenity,
    ExploreCities,
    BenefitSection,
    PropertyType,
    Testimonial,
    Agent,
    FAQ,
    FAQPage,
    ContactPage,
    PricingPage,
    PricingPlan,
    ServicePage,
    Service,
    User,
)
from django.views.generic import ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import LoginForm, RegisterForm
import math, json

class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # duplicate_property()
        context.update({
            "all_properties": Property.objects.order_by("-created_at")[:6],
            "apartments": Property.objects.filter(property_types__name="apartment").order_by("-created_at")[:6],
            "villas": Property.objects.filter(property_types__name="villa").order_by("-created_at")[:6],
            "studios": Property.objects.filter(property_types__name="studio").order_by("-created_at")[:6],
            "houses": Property.objects.filter(property_types__name="townhouse").order_by("-created_at")[:6],
            "offices": Property.objects.filter(property_types__name="office").order_by("-created_at")[:6],
            "top_properties": Property.objects.filter(property_types__name="office").order_by("-created_at")[:6],
            "explore_cities": ExploreCities.objects.all().order_by("-id"),
            "benefit_section": BenefitSection.objects.first(),
            "services": Service.objects.filter(is_active=True),
            "testimonial_section": Testimonial.objects.all()[:10],
            "agents": Agent.objects.filter(is_active=True, is_visble=True)[:4]
        })
        return context

class AboutUsView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            "testimonial_section": Testimonial.objects.all()[:3],
            "agents": Agent.objects.filter(is_active=True, is_visble=True)[:4]
        }
        return context

class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("contact_us")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = ContactPage.objects.first()
        context["faqs"] = FAQ.objects.filter(is_active=True)
        return context

class PricingView(TemplateView):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = PricingPage.objects.first()
        context["faqs"] = FAQ.objects.filter(is_active=True)
        context["plans"] = PricingPlan.objects.all()
        return context

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ContactMessageForm()
        amenities = list(PropertyAmenity.objects.filter(property=self.object))
        total = len(amenities)
        per_col = math.ceil(total / 3) if total else 0
        context['amenity_columns'] = [
            amenities[0:per_col],
            amenities[per_col:per_col * 2],
            amenities[per_col * 2:per_col * 3],
        ]
        context['latest_properties'] = (
            Property.objects
            .exclude(id=self.object.id)
            .order_by('-created_at')[:5]
        )

        return context

class PropertyListView(ListView):
    model = Property
    template_name = "property_list.html"
    context_object_name = "properties"
    paginate_by = 12

    def get_queryset(self):
        queryset = Property.objects.order_by('-id').all().prefetch_related("images")

        # -------- FILTERS --------
        status = self.request.GET.get("status")
        property_type = self.request.GET.get("type")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if status:
            queryset = queryset.filter(property_status=status)

        if property_type:
            queryset = queryset.filter(property_types__name=property_type)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "grid")

        properties = Property.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )

        context["map_properties"] = json.dumps([
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "price": float(p.price),  # 🔥 FIX
            }
            for p in properties
        ])
        print(context["map_properties"])

        return context

class FAQView(ListView):
    model = FAQ
    template_name = "faq.html"
    context_object_name = "faq"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = FAQPage.objects.first()
        faqs = FAQ.objects.filter(is_active=True)

        categories = {
            "overview": "Overview",
            "costs": "Costs and Payments",
            "safety": "Safety and Security",
        }

        context = {
            "page": page,
            "faqs": faqs,
            "categories": categories,
        }
        return context

class ServiceView(TemplateView):
    template_name = "service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = ServicePage.objects.first()
        context["services"] = Service.objects.filter(is_active=True)
        context["faqs"] = FAQ.objects.filter(is_active=True)
        context["testimonial_section"] = Testimonial.objects.all()

        return context


class RegisterView(TemplateView):
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"]= RegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["mobile"],
                password=form.cleaned_data["password"]
            )
            return redirect("login")
        context = self.get_context_data()
        context["register_form"] = form
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"]= LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            print("user", user)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
        context = self.get_context_data()
        context["login_form"] = form
        return self.render_to_response(context)

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("about_us")


class PropertyAddView(TemplateView):
    template_name = "add_property.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = ServicePage.objects.first()
        context["services"] = Service.objects.filter(is_active=True)
        context["faqs"] = FAQ.objects.filter(is_active=True)
        context["testimonial_section"] = Testimonial.objects.all()

        return context

from django.http import JsonResponse
from django.db.models import Q

def property_types(request):
    preference = request.GET.get('preference', 'sell').lower()
    category = request.GET.get('category', 'residential').lower()
    if preference == "pg": category = "residential"
    types_qs = PropertyType.objects.filter(category=category)    
    types_qs = PropertyType.objects.filter(category=category).filter(
        Q(preference__isnull=True) | Q(preference=preference)
    )
    types_list = list(types_qs.values_list('name', flat=True))
    return JsonResponse({
        "success": True,
        "preference": preference,
        "category": category,
        "types": types_list
    })


# def property_create(request):
#     print(request.POST)
#     files = request.FILES

#     return JsonResponse({
#         "success": True,
#     })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PropertyType
from .serializers import PropertySerializer

class CreatePropertyAPIView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data)

        serializer = PropertySerializer(
            data=data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Property created successfully"}, status=201)
        
        print(serializer.errors)
        return Response(serializer.errors, status=400)

# Create your views here.
