from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import AnalyzedString

class AnalyzerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_retrieve(self):
        url = reverse('create_or_list')  # ensure your URL pattern has name='create_or_list'
        res = self.client.post(url, {"value": "madam"}, format="json")
        self.assertEqual(res.status_code, 201)
        body = res.json()
        self.assertIn("id", body)
        self.assertIn("properties", body)
        self.assertTrue(body["properties"]["is_palindrome"])

        # retrieve
        get_url = reverse('get_string', args=["madam"])  # ensure URL pattern named 'get_string'
        url = reverse('get_string', args=["madam"])
        print("URL being tested:", url)
        res2 = self.client.get(url)
        res2 = self.client.get(get_url)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()["value"], "madam")

    def test_conflict_on_duplicate(self):
        url = reverse('create_or_list')
        self.client.post(url, {"value": "hello"}, format="json")
        res = self.client.post(url, {"value": "hello"}, format="json")
        self.assertEqual(res.status_code, 409)

    def test_nl_parser(self):
        # Create two single-word palindromes
        url = reverse('create_or_list')
        self.client.post(url, {"value": "madam"}, format="json")
        self.client.post(url, {"value": "civic"}, format="json")
        
        filter_url = reverse('nl_filter')  # ensure your URL pattern has name='nl_filter'
        res = self.client.get(
            f"{filter_url}?query=all%20single%20word%20palindromic%20strings"
        )
        self.assertEqual(res.status_code, 200)
        j = res.json()
        self.assertEqual(j["count"], 2)
        # Additional check: ensure returned strings are correct
        values = [item["value"] for item in j["data"]]
        self.assertIn("madam", values)
        self.assertIn("civic", values)