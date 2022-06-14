from rest_framework import routers
from companies.views.api_company import CompanyViewSet

companies_router = routers.DefaultRouter()

companies_router.register("companies", viewset=CompanyViewSet, basename="companies")