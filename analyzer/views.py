from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AnalyzedString
from .serializers import AnalyzeSerializer, AnalyzedStringSerializer
from .filters import AnalyzedStringFilter
from .utils import analyze_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from datetime import datetime
import re

class AnalyzeStringView(APIView):
    def post(self, request):
        serializer = AnalyzeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)
        
        value = serializer.validated_data.get("value")
        if not isinstance(value, str):
            return Response({"error": "value must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        hash_id = analyze_string(value)["sha256_hash"]
        if AnalyzedString.objects.filter(id=hash_id).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        properties = analyze_string(value)
        obj = AnalyzedString.objects.create(id=hash_id, value=value, properties=properties)
        response = AnalyzedStringSerializer(obj)
        return Response(response.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        query_params = {k: v.strip() if isinstance(v, str) else v for k, v in request.GET.items()}
        queryset = AnalyzedString.objects.all()
        params = request.query_params

        # Apply filters
        if "is_palindrome" in query_params:
            queryset = queryset.filter(properties__is_palindrome=query_params["is_palindrome"].lower() == "true")

        if "min_length" in query_params:
            queryset = queryset.filter(properties__length__gte=int(query_params["min_length"]))

        if "max_length" in query_params:
            queryset = queryset.filter(properties__length__lte=int(query_params["max_length"]))

        if "word_count" in query_params:
            queryset = queryset.filter(properties__word_count=int(query_params["word_count"]))

        if "contains_character" in query_params:
            contains_char = query_params["contains_character"]
            queryset = queryset.filter(value__icontains=contains_char)

        data = list(queryset.values("id", "value", "properties", "created_at"))
        return Response({
            "data": data,
            "count": len(data),
            "filters_applied": query_params
        })
    

class GetAllStringsView(generics.ListAPIView):
    queryset = AnalyzedString.objects.all().order_by('-created_at')
    serializer_class = AnalyzedStringSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnalyzedStringFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        filters_applied = {k: v for k, v in request.query_params.items()}
        response.data = {
            "data": response.data,
            "count": len(response.data),
            "filters_applied": filters_applied
        }
        return response


class GetSpecificStringView(APIView):
    def get(self, request, string_value):
        try:
            obj = AnalyzedString.objects.get(value=string_value)
            serializer = AnalyzedStringSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "String not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, string_value):
        try:
            obj = AnalyzedString.objects.get(value=string_value)
            obj.delete()
            return Response({"message": f"'{string_value}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "String not found."}, status=status.HTTP_404_NOT_FOUND)

class NaturalLanguageFilterView(APIView):
    def parse_query(self, query):
        filters = {}

        # Detect palindrome
        if re.search(r"\bpalindrom(ic|e)?\b", query):
            filters["is_palindrome"] = True

        # Word count
        if "single word" in query:
            filters["word_count"] = 1
        elif match := re.search(r"(\d+)\s+words?", query):
            filters["word_count"] = int(match.group(1))

        # Length filters
        if match := re.search(r"longer than (\d+)", query):
            filters["min_length"] = int(match.group(1)) + 1
        if match := re.search(r"shorter than (\d+)", query):
            filters["max_length"] = int(match.group(1)) - 1
        if match := re.search(r"(exactly|with length)\s+(\d+)", query):
            length = int(match.group(2))
            filters["min_length"] = length
            filters["max_length"] = length

        # Character containment
        if match := re.search(r"containing (?:the letter )?([a-z])", query):
            filters["contains_character"] = match.group(1)

        # First vowel
        if "first vowel" in query:
            filters["contains_character"] = "a"

        return filters

    def get(self, request):
        query = request.query_params.get("query", "").lower().strip()
        if not query:
            return Response({"error": "Missing 'query' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed_filters = self.parse_query(query)

            # Check for conflicting filters
            if (
                "min_length" in parsed_filters and
                "max_length" in parsed_filters and
                parsed_filters["min_length"] > parsed_filters["max_length"]
            ):
                return Response({"error": "Conflicting filters detected."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not parsed_filters:
                return Response({"error": "Unable to parse natural language query."}, status=status.HTTP_400_BAD_REQUEST)

            # Apply filters
            qs = AnalyzedString.objects.all()
            if "is_palindrome" in parsed_filters:
                qs = qs.filter(properties__is_palindrome=parsed_filters["is_palindrome"])
            if "word_count" in parsed_filters:
                qs = qs.filter(properties__word_count=parsed_filters["word_count"])
            if "min_length" in parsed_filters:
                qs = qs.filter(properties__length__gte=parsed_filters["min_length"])
            if "max_length" in parsed_filters:
                qs = qs.filter(properties__length__lte=parsed_filters["max_length"])
            if "contains_character" in parsed_filters:
                qs = qs.filter(value__icontains=parsed_filters["contains_character"])

            serializer = AnalyzedStringSerializer(qs, many=True)
            return Response({
                "data": serializer.data,
                "count": len(serializer.data),
                "interpreted_query": {
                    "original": query,
                    "parsed_filters": parsed_filters
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unable to parse natural language query: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)