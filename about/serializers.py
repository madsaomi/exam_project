from rest_framework import serializers
from .models import AboutContent


class AboutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContent
        fields = '__all__'
        read_only_fields = ('updated_at',)
