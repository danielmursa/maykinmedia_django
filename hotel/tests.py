from django.test import TestCase
from .models import City, Hotel
from .utils import import_cities, import_hotels


class ImportCitiesTestCase(TestCase):
    """
    Tests for the `import_cities` function.
    """

    def test_city_success(self):
        """
        Test importing new cities with unique codes.

        Verifies that new cities are created and no errors occur.
        """
        lines = [["MIL", "Milano"], ["BOL", "Bologna"]]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["total_cities"], 2)
        self.assertEqual(stats["created_cities"], 2)
        self.assertEqual(stats["updated_cities"], 0)
        self.assertEqual(stats["errors"], 0)

        self.assertTrue(City.objects.filter(code="BOL").exists())
        self.assertTrue(City.objects.filter(code="MIL").exists())

    def test_city_duplicate(self):
        """
        Test importing a city with an existing code.

        Ensures that the existing city is updated and no new cities are created.
        """
        City.objects.create(code="BOL", name="Bologna")

        lines = [["BOL", "Bologna"]]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["total_cities"], 1)
        self.assertEqual(stats["created_cities"], 0)
        self.assertEqual(stats["updated_cities"], 1)
        self.assertEqual(stats["errors"], 0)

        self.assertTrue(City.objects.filter(code="BOL").exists())

    def test_city_error(self):
        """
        Test importing cities with incorrect codes.

        Verifies that errors are handled and no invalid cities are created.
        """
        lines = [["BOLOGNA", "Bologna"]]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["errors"], 1)
        self.assertEqual(stats["total_cities"], 1)
        self.assertEqual(stats["created_cities"], 0)
        self.assertEqual(stats["updated_cities"], 0)

        self.assertFalse(City.objects.all().exists())
        self.assertFalse(City.objects.filter(code="BOL").exists())


class ImportHotelsTestCase(TestCase):
    """
    Tests for the `import_hotels` function.
    """

    def test_hotel_success(self):
        """
        Test importing hotels after cities are created.

        Verifies that hotels are created successfully when cities exist.
        """
        lines = [["MIL", "Milano"], ["BOL", "Bologna"]]

        success, stats = import_cities(lines)
        self.assertTrue(City.objects.filter(code="BOL").exists())
        self.assertTrue(City.objects.filter(code="MIL").exists())

        lines = [
            ["MIL", "MIL01", "Milano 1"],
            ["MIL", "MIL02", "Milano 2"],
            ["BOL", "BOL01", "Bologna 1"],
            ["BOL", "BOL02", "Bologna 2"],
        ]

        success, stats = import_hotels(lines)
        self.assertTrue(success)
        self.assertEqual(stats["errors"], 0)
        self.assertEqual(stats["total_hotels"], 4)
        self.assertEqual(stats["created_hotels"], 4)
        self.assertEqual(stats["updated_hotels"], 0)

        self.assertTrue(Hotel.objects.filter(code="MIL01").exists())
        self.assertTrue(Hotel.objects.filter(code="MIL02").exists())
        self.assertTrue(Hotel.objects.filter(code="BOL01").exists())
        self.assertTrue(Hotel.objects.filter(code="BOL02").exists())

    def test_city_hotel_related_success(self):
        """
        Test that hotels are related to the correct city.

        Verifies that hotels are linked to their respective cities and the
        relationships are correctly set.
        """
        lines = [["MIL", "Milano"], ["BOL", "Bologna"]]
        success, stats = import_cities(lines)
        
        lines = [
            ["MIL", "MIL01", "Milano 1"],
            ["MIL", "MIL02", "Milano 2"],
            ["BOL", "BOL01", "Bologna 1"],
            ["BOL", "BOL02", "Bologna 2"],
        ]
        success, stats = import_hotels(lines)

        self.assertEqual(
            Hotel.objects.filter(code="MIL01").first().city,
            City.objects.get(code="MIL"),
        )
        self.assertEqual(City.objects.get(code="MIL").hotels.count(), 2)
        self.assertEqual(City.objects.all().count(), 2)
        self.assertEqual(Hotel.objects.all().count(), 4)

    def test_hotel_error(self):
        """
        Test importing hotels with non-existent city codes.

        Ensures that hotels are not created if their related city does not exist.
        """
        lines = [["MIL", "MILANO"]]

        success, stats = import_cities(lines)
        lines = [
            ["BOL", "BOL01", "Bologna 1"],
            ["BOL", "BOL02", "Bologna 2"],
        ]
        success, stats = import_hotels(lines)
        self.assertTrue(success)
        self.assertEqual(stats["errors"], 2)
        self.assertEqual(stats["total_hotels"], 2)
        self.assertEqual(stats["created_hotels"], 0)
        self.assertEqual(stats["updated_hotels"], 0)

        self.assertFalse(Hotel.objects.filter(code="BOL01").exists())
        self.assertFalse(Hotel.objects.filter(code="BOL02").exists())
