import django_filters
from reviews_app.models import Review

class ReviewFilter(django_filters.FilterSet):
    """

    FilterSet for Review model to filter reviews based on:
    
    - business_user_id: Filters reviews for a specific business user (foreign key).
    - reviewer_id: Filters reviews created by a specific reviewer (foreign key).

    Usage:
    - Can be used in Django REST Framework views to filter queryset by these fields.
    
    """
    business_user = django_filters.NumberFilter(field_name='business_user')
    reviewer = django_filters.NumberFilter(field_name='reviewer')

    class Meta:
        model = Review
        fields = ['business_user', 'reviewer']