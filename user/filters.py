from audioop import avg
from django_filters.rest_framework import FilterSet, ChoiceFilter, NumberFilter, CharFilter, BooleanFilter
from django.db.models import Q, Avg

from .models import Gofer


class GoferFilterSet(FilterSet):
    category = CharFilter(field_name='sub_category__category__category_name', method='filter_by_category')
    state = CharFilter(field_name='custom_user__address__state', method='filter_by_state')
    country = CharFilter(field_name='custom_user__address__country', method='filter_by_country')
    gender = CharFilter(field_name='custom_user__gender', method='filter_by_gender')
    charges_above = NumberFilter(field_name='charges', lookup_expr='gt')
    charges_below = NumberFilter(field_name='charges', lookup_expr='lt')
    avg_rating = NumberFilter(field_name='avg_rating', lookup_expr='gte')
    is_available = BooleanFilter(field_name='is_available')

    class Meta:
        model = Gofer
        fields = {
            'expertise',
            'avg_rating', 'is_available',
        }
        
    def filter_by_state(self, queryset, name, value):
        return queryset.filter(
            Q(custom_user__address__state__icontains=value)
        )
    def filter_by_country(self, queryset, name, value):
        return queryset.filter(
            Q(custom_user__address__country__icontains=value)
        )
    
    def filter_by_category(self, queryset, name, value):
        return queryset.filter(sub_category__category__category_name__icontains=value)    
    
    def filter_by_gender(self, queryset, name, value):
        return queryset.filter(custom_user__gender=value)
    
    def filter_queryset(self, queryset):
        filter_conditions = Q()
        
        if 'category' in self.form.cleaned_data and self.form.cleaned_data['category']:
            filter_conditions |= Q(sub_category__category__category_name__icontains=self.form.cleaned_data['category'])
            
        if 'state' in self.form.cleaned_data and self.form.cleaned_data['state']:
            filter_conditions |= Q(custom_user__address__state__icontains=self.form.cleaned_data['state'])
            
        if 'country' in self.form.cleaned_data and self.form.cleaned_data['country']:
            filter_conditions |= Q(custom_user__address__country__icontains=self.form.cleaned_data['country'])

        if 'expertise' in self.form.cleaned_data and self.form.cleaned_data['expertise']:
            filter_conditions |= Q(expertise__icontains=self.form.cleaned_data['expertise'])
            
        if 'gender' in self.form.cleaned_data and self.form.cleaned_data['gender']:
            filter_conditions &= Q(custom_user__gender__icontains=self.form.cleaned_data['gender'])

        if 'mobility_means' in self.form.cleaned_data and self.form.cleaned_data['mobility_means']:
            filter_conditions &= Q(mobility_means=self.form.cleaned_data['mobility_means'])

        if 'charges_above' in self.form.cleaned_data and self.form.cleaned_data['charges_above']:
            filter_conditions |= Q(charges__gt=self.form.cleaned_data['charges_above'])

        if 'charges_below' in self.form.cleaned_data and self.form.cleaned_data['charges_below']:
            filter_conditions |= Q(charges__lt=self.form.cleaned_data['charges_below'])
            
        if 'is_available' in self.form.cleaned_data and self.form.cleaned_data['is_available']:
            filter_conditions &= Q(is_available__exact=self.form.cleaned_data['is_available'])

        # if 'min_rating' in self.form.cleaned_data and self.form.cleaned_data['min_rating']:
        #     filter_conditions |= Q(avg_rating__gte=self.form.cleaned_data['min_rating'])

        return queryset.filter(filter_conditions)

    # def filter_queryset(self, queryset):
    #     # Custom logic to ensure at least one condition is met
    #     conditions = Q()
    #     print(self.form.cleaned_data.items())
    #     print(callable(self.filters['sub_category'].method))
    #     for name, value in self.form.cleaned_data.items():
    #         if value:
    #             filter_method = self.filters[name].method
    #             if not callable(filter_method):
    #                 if filter_method in globals() and callable(globals()[filter_method]):
    #                     conditions |= globals()[filter_method](queryset, name, value).query
    #             else:
    #                 lookup_expr = self.filters[name].lookup_expr
    #                 field_name = self.filters[name].field_name
    #                 conditions |= Q(**{f"{field_name}__{lookup_expr}": value})
    #     print(conditions)
    #     return queryset.filter(conditions)