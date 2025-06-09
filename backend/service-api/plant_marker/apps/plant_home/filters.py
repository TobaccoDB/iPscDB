import django_filters
from django.db.models import Q
from .models import *


class CellSearchFilter(django_filters.FilterSet):
    """
   Sample Search Filter
    """
    # species_name = django_filters.CharFilter(method='species_name_eq')
    # tissue = django_filters.CharFilter(method='tissue_eq')
    # project_id = django_filters.CharFilter(method='project_id_eq')
    # sample_id = django_filters.CharFilter(method='sample_id_eq')
    search = django_filters.CharFilter(method='search_keyword')

    class Meta:
        model = Sample
        fields = ['sam_id', 'sample_id', 'project_id', 'species_name', 'tissue', 'chemistry', 'lit_id']

    def search_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(species_name=value) | Q(tissue=value) | Q(project_id__icontains=value) | Q(sample_id__icontains=value))
