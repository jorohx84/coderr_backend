import django_filters
from django.db.models import Min
from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        # Filtert alle Offers, bei denen der minimale Preis >= value ist
        return queryset.annotate(min_price=Min('details__price')).filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        # Filtert alle Offers, bei denen die minimale Lieferzeit <= value ist
        return queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days')).filter(min_delivery_time__lte=value)
