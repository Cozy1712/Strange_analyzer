# import django_filters
# from .models import AnalyzedString

# class AnalyzedStringFilter(django_filters.FilterSet):
#     is_palindrome = django_filters.BooleanFilter(method="filter_is_palindrome")
#     min_length = django_filters.NumberFilter(field_name="properties", method="filter_min_length")
#     max_length = django_filters.NumberFilter(field_name="properties", method="filter_max_length")
#     word_count = django_filters.NumberFilter("filter_word_count")
#     contains_character = django_filters.CharFilter(method="filter_contains_character")

#     class Meta:
#         model = AnalyzedString
#         fields = [] # all filtering is done via manual methods

#         def filter_is_palindrome(self, queryset, name, value):
#             return queryset.filter(**{f"properties__is__palindrome": value}) # filter by palindrome property
        
#         def filter_min_length(self, queryset, name, value):
#             return queryset.filter(**{f"properties__length__gte": value}) # greater than or equal to min_length
        
#         def filter_max_length(self, queryset, name, value):
#             return queryset.filter(**{f"properties__length__lte": value}) # less than or equal to max_length
        
#         def filter_word_count(self, queryset, name, value):
#             return queryset.filter(**{"properties__word__count": value}) # exact match for word count
        
#         def filter_contains_character(self, queryset, name, value):
#             if not value or len(value) != 1:
#                 # Invalid character filter
#                 return queryset.none()
#             return queryset.filter(value__contains=value)
        

import django_filters
from .models import AnalyzedString

class AnalyzedStringFilter(django_filters.FilterSet):
    is_palindrome = django_filters.BooleanFilter(field_name='properties__is_palindrome')
    min_length = django_filters.NumberFilter(field_name='properties__length', lookup_expr='gte')
    max_length = django_filters.NumberFilter(field_name='properties__length', lookup_expr='lte')
    word_count = django_filters.NumberFilter(field_name='properties__word_count')
    contains_character = django_filters.CharFilter(method='filter_contains_character')

    class Meta:
        model = AnalyzedString
        fields = ['is_palindrome', 'min_length', 'max_length', 'word_count', 'contains_character']

    def filter_contains_character(self, queryset, name, value):
        return queryset.filter(value__icontains=value)
