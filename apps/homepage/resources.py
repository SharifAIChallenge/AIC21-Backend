from import_export import resources

from .models import Subscribe


class SubscribeResource(resources.ModelResource):
    class Meta:
        model = Subscribe
        fields = ('email',)
