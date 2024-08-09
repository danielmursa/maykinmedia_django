import csv
import logging
import requests
from io import StringIO
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import City, Hotel
from .settings import *

logger = logging.getLogger(__name__)


def get_api_credentials():
    """
    Retrieve API credentials for the 'api_user'.
    Attempts to fetch the API credentials (username and password) for the user with the username 'api_user'.

    Returns:
        tuple: (str, str) The API credentials (username, password) or empty strings.
    """
    try:
        user_api = User.objects.get(username="api_user")
        return (user_api.first_name, user_api.last_name)
    except:
        return ("", "")


def make_request(url):
    """
    Makes a GET request to the specified URL and returns an iterator over the response lines.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
    """
    try:
        # credentials = get_api_credentials()
        # response = requests.get(url, auth=credentials)
        # you can access at the API even without a credentials
        logger.debug(f"Make request for {url}")
        response = requests.get(url)
        response.raise_for_status()
        csv_file = StringIO(response.text)
        csv_reader = csv.reader(csv_file, delimiter=";")
        return [row for row in csv_reader]
    except requests.RequestException as e:
        logger.error(f"Error during request for {url}, {e}")
        return []


def import_cities(lines=""):
    """
    Import cities from an external API and update the database.
    Fetches city data from an API, processes each line, and updates or creates City objects in the database.
    Collects and returns import statistics.

    Returns:
        tuple: (bool, dict) A boolean indicating success or failure, and a dictionary with import statistics or error details.
    """
    total_cities = 0
    updated_cities = 0
    created_cities = 0
    errors = 0

    try:
        if not lines:
            lines = make_request(API_URL_CITY)
        for line in lines:
            total_cities += 1
            try:
                city, created = City.objects.update_or_create(
                    code=line[0], defaults={"name": line[1]}
                )
                if created:
                    logger.debug(f"Create new city {city}")
                    created_cities += 1
                else:
                    logger.debug(f"Update city {city}")
                    updated_cities += 1
            except IntegrityError as e:
                errors += 1
            except Exception as e:
                errors += 1

        stats = {
            "total_cities": total_cities,
            "created_cities": created_cities,
            "updated_cities": updated_cities,
            "errors": errors,
        }

        return True, stats

    except requests.RequestException as e:
        logger.error(f"Error {e}")
        return False, {
            "error_code": 2,
            "message": f"Errore durante la richiesta API: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Error {e}")
        return False, {
            "error_code": 3,
            "message": f"Errore durante l'importazione: {str(e)}",
        }


def import_hotels(lines=""):
    """
    Import hotels from an external API and update the database.
    Fetches Hotel data from an API, processes each line, and updates or creates Hotel objects in the database.
    Collects and returns import statistics.

    Returns:
        tuple: (bool, dict) A boolean indicating success or failure, and a dictionary with import statistics or error details.
    """
    total_hotels = 0
    updated_hotels = 0
    created_hotels = 0
    errors = 0

    try:
        if not lines:
            lines = make_request(API_URL_HOTEL)
        for line in lines:
            total_hotels += 1
            try:
                city = City.objects.filter(code=line[0]).first()
                if city:
                    hotel, created = Hotel.objects.update_or_create(
                        city=city, code=line[1], defaults={"name": line[2]}
                    )
                    if created:
                        logger.debug(f"Create new hotel {hotel}")
                        created_hotels += 1
                    else:
                        logger.debug(f"Update hotel {hotel}")
                        updated_hotels += 1
                else:
                    errors += 1
            except IntegrityError as e:
                errors += 1
            except Exception as e:
                errors += 1

        stats = {
            "total_hotels": total_hotels,
            "created_hotels": created_hotels,
            "updated_hotels": updated_hotels,
            "errors": errors,
        }

        return True, stats

    except requests.RequestException as e:
        logger.error(f"Error {e}")
        return False, {
            "error_code": 2,
            "message": f"Errore durante la richiesta API: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Error {e}")
        return False, {
            "error_code": 3,
            "message": f"Errore durante l'importazione: {str(e)}",
        }
