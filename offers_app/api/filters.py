import django_filters
from django.db.models import Min
from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    """
    FilterSet for filtering Offer objects based on creator, price, and delivery time.

    Supported filters:
    - creator_id: Filters offers by the user ID of the creator (`user__id`).
    - min_price: Filters offers where the minimum price across all related details is greater than or equal to the given value.
    - max_delivery_time: Filters offers where the minimum delivery time across all related details is less than or equal to the given value.
    
    """

    creator_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(min_price=Min('details__price')).filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days')).filter(min_delivery_time__lte=value)
