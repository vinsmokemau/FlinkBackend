"""Company tests."""

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from apps.companies.models import Company

# Utilities
from decimal import Decimal


class CompanyTests(APITestCase):
    """Test case class to validate project's logic requirements.
    Creation:
        - Company name's limit up to 50 chars.
        - Company description's limit up to 100 chars
        - Company symbol's limit up to 100 chars
        - Company's symbol in the NYSE
    Update:
        - Update Principal Fields
            - Name
            - Description
        - Add Market Value
            - Add a new decimal value to the list of market values
        - Change Status
            - Company can be activated or deactivated.
    List:
        - Base filtering: is_active in True
        - Fields included:
            id, name, description, symbol, market_values, created_at, updated_at
    """

    def setUp(self):
        """Test case setup."""

        # Request Data
        self.url = "/companies/"
        self.payload = {
            "name": "Meta Platforms, Inc.",
            "description": "Meta Platforms Inc, formerly Facebook is the world's largest online social network.",
            "symbol": "FB",
            "value": 301.71
        }

        # Company Setup
        self.company = Company.objects.create(
            name="Amazon.com, Inc",
            description="Amazon.com Inc is a leading online retailer and one of the highest-grossing e-commerce aggregators",
            symbol="AMZN",
            market_values=[2988.01],
        )
        self.company_url = self.url + f"{self.company.id}/"

    def test_response_success(self):
        """Verify request succeed."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_company(self):
        """Verify the creation of a company succesfully."""
        request = self.client.post(self.url, self.payload)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_missing_fields_create_company(self):
        """Verify the not creation of a company by missing fields."""

        # Without Name
        no_name_payload = self.payload.copy()
        no_name_payload.pop("name")
        no_name_request = self.client.post(self.url, no_name_payload)
        self.assertEqual(no_name_request.status_code, status.HTTP_400_BAD_REQUEST)

        # Without Description
        no_description_payload = self.payload.copy()
        no_description_payload.pop("description")
        no_description_request = self.client.post(self.url, no_description_payload)
        self.assertEqual(no_description_request.status_code, status.HTTP_400_BAD_REQUEST)

        # Without Symbol
        no_symbol_payload = self.payload.copy()
        no_symbol_payload.pop("symbol")
        no_symbol_request = self.client.post(self.url, no_symbol_payload)
        self.assertEqual(no_symbol_request.status_code, status.HTTP_400_BAD_REQUEST)

        # Without Value
        no_value_payload = self.payload.copy()
        no_value_payload.pop("value")
        no_value_request = self.client.post(self.url, no_value_payload)
        self.assertEqual(no_value_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exceed_limits_create_company(self):
        """Verify the not creation of a company by exceeding limits."""

        # Exceed Name Limit
        no_name_payload = self.payload.copy()
        no_name_payload["name"] = no_name_payload["name"] * 50
        no_name_request = self.client.post(self.url, no_name_payload)
        self.assertEqual(no_name_request.status_code, status.HTTP_400_BAD_REQUEST)

        # Exceed Description Limit
        no_description_payload = self.payload.copy()
        no_description_payload["description"] = no_description_payload["description"] * 100
        no_description_request = self.client.post(self.url, no_description_payload)
        self.assertEqual(no_description_request.status_code, status.HTTP_400_BAD_REQUEST)

        # Exceed Symbol Limit
        no_symbol_payload = self.payload.copy()
        no_symbol_payload["symbol"] = no_symbol_payload["symbol"] * 10
        no_symbol_request = self.client.post(self.url, no_symbol_payload)
        self.assertEqual(no_symbol_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_nyse_symbol_create_company(self):
        """Verify the not creation of a company by a non-NYSE symbol."""
        self.payload["symbol"] = "NO-SYMBOL"
        request = self.client.post(self.url, self.payload)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deactivate_company(self):
        """Verify the deactivation of a company."""
        test_payload = {"is_active": False}
        test_url = self.company_url + "change_status/"
        request = self.client.patch(test_url, test_payload)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.is_active, False)

    def test_update_info_company(self):
        test_payload = {
            "name": "Tesla, Inc",
            "description": "Tesla is a vertically integrated sustainable energy company and electric vehicles",
        }
        request = self.client.patch(self.company_url, test_payload)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, test_payload["name"])
        self.assertEqual(self.company.description, test_payload["description"])

    def test_add_value_company(self):
        test_payload = {
            "value": 3005.81
        }
        request = self.client.patch(self.company_url, test_payload)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.market_values[-1], Decimal(str(test_payload["value"])))
