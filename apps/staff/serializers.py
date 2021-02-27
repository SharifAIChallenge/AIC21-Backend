from django.conf import settings

from rest_framework import serializers

from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('_get_image')

    @staticmethod
    def _get_image(obj: Staff):
        url = obj.image.url
        if settings.DOMAIN not in url:
            return settings.DOMAIN + url
        return url

    class Meta:
        model = Staff
        fields = ['group_title', 'team_title', 'first_name_en',
                  'first_name_fa', 'last_name_en', 'last_name_fa', 'url',
                  'image', 'role']
