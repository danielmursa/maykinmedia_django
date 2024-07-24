from django.test import TestCase
from .models import City, Hotel
from .utils import import_cities, import_hotels


class ImportCitiesTestCase(TestCase):
    def test_city_success(self):
        lines = [b"MIL;Milano", b"BOL;Bologna"]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["total_cities"], 2)
        self.assertEqual(stats["created_cities"], 2)
        self.assertEqual(stats["updated_cities"], 0)
        self.assertEqual(stats["errors"], 0)

        self.assertTrue(City.objects.filter(code="BOL").exists())
        self.assertTrue(City.objects.filter(code="MIL").exists())

    def test_city_duplicate(self):
        City.objects.create(code="BOL", name="Bologna")

        lines = [b"BOL; Bologna"]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["total_cities"], 1)
        self.assertEqual(stats["created_cities"], 0)
        self.assertEqual(stats["updated_cities"], 1)
        self.assertEqual(stats["errors"], 0)

        self.assertTrue(City.objects.filter(code="BOL").exists())

    def test_city_error(self):
        # City code wrong
        lines = [b"BOLOGNA; Bologna"]

        success, stats = import_cities(lines)

        self.assertTrue(success)
        self.assertEqual(stats["errors"], 1)
        self.assertEqual(stats["total_cities"], 1)
        self.assertEqual(stats["created_cities"], 0)
        self.assertEqual(stats["updated_cities"], 0)

        self.assertFalse(City.objects.all().exists())
        self.assertFalse(City.objects.filter(code="BOL").exists())


class ImportHotelsTestCase(TestCase):
    def test_hotel_success(self):
        lines = [b"MIL;Milano", b"BOL;Bologna"]

        success, stats = import_cities(lines)
        self.assertTrue(City.objects.filter(code="BOL").exists())
        self.assertTrue(City.objects.filter(code="MIL").exists())

        lines = [
            b"MIL;MIL01;Milano 1",
            b"MIL;MIL02;Milano 2",
            b"BOL;BOL01;Bologna 1",
            b"BOL;BOL02;Bologna 2",
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
        lines = [b"MIL;Milano", b"BOL;Bologna"]
        success, stats = import_cities(lines)

        lines = [
            b"MIL;MIL01;Milano 1",
            b"MIL;MIL02;Milano 2",
            b"BOL;BOL01;Bologna 1",
            b"BOL;BOL02;Bologna 2",
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
        # City not found
        lines = [
            b"MIL;Milano",
        ]

        success, stats = import_cities(lines)
        lines = [
            b"BOL;BOL01;Bologna 1",
            b"BOL;BOL02;Bologna 2",
        ]
        success, stats = import_hotels(lines)
        self.assertTrue(success)
        self.assertEqual(stats["errors"], 2)
        self.assertEqual(stats["total_hotels"], 2)
        self.assertEqual(stats["created_hotels"], 0)
        self.assertEqual(stats["updated_hotels"], 0)

        self.assertFalse(Hotel.objects.filter(code="BOL01").exists())
        self.assertFalse(Hotel.objects.filter(code="BOL02").exists())
