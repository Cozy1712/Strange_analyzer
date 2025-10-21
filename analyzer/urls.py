from django.urls import path
from .views import AnalyzeStringView, GetSpecificStringView, NaturalLanguageFilterView

urlpatterns = [
    # path("strings/all", GetAllStringsView.as_view(), name="list_strings"),
    path("strings", AnalyzeStringView.as_view(), name="create_or_list"),
    # path("strings/<str:string_value>", GetSpecificStringView.as_view(), name="get_string"),
    path("strings/<str:string_value>", GetSpecificStringView.as_view(), name="get_or_delete_string"),
    path("strings/filter-by-natural-language", NaturalLanguageFilterView.as_view(), name="nl_filter"),  
]