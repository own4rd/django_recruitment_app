from django.contrib import admin
from django.urls import include, path
from companies.views.api_company import send_company_email
from companies.urls import companies_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(companies_router.urls)),
    path("send-email", send_company_email),
]
