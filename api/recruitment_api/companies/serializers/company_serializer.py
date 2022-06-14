from rest_framework import serializers
from companies.models.company import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "status", "application_link", "last_update", "notes"]
