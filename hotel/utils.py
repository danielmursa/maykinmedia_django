import requests
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import City, Hotel
from .settings import *


def clean_line(line):
    """
    Clean and parse a line of data. Decodes a byte string, removes any double quotes, and splits the line by semicolons into a list of strings.

    Args:
        line (bytes): A line of data in bytes.

    Returns:
        list: A list of strings obtained by splitting the cleaned line.
    """
    return line.decode().replace('"', "").split(";")


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


def import_cities():
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
        credentials = get_api_credentials()
        response = requests.get(API_URL_CITY, auth=credentials)
        response.raise_for_status()
        for line in response.iter_lines():
            total_cities += 1
            try:
                line = clean_line(line)
                city, created = City.objects.update_or_create(
                    code=line[0], defaults={"name": line[1]}
                )
                if created:
                    created_cities += 1
                else:
                    updated_cities += 1
            except IntegrityError as e:
                errors += 1
                print(f"Integrity error for line {line}: {str(e)}")
            except Exception as e:
                errors += 1
                print(f"Error processing line {line}: {str(e)}")

        stats = {
            "total_cities": total_cities,
            "created_cities": created_cities,
            "updated_cities": updated_cities,
            "errors": errors,
        }

        return True, stats

    except requests.RequestException as e:
        return False, {
            "error_code": 2,
            "message": f"Errore durante la richiesta API: {str(e)}",
        }
    except Exception as e:
        return False, {
            "error_code": 3,
            "message": f"Errore durante l'importazione: {str(e)}",
        }


def import_hotels():
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
        credentials = get_api_credentials()
        response = requests.get(API_URL_HOTEL, auth=credentials)
        response.raise_for_status()
        for line in response.iter_lines():
            total_hotels += 1
            try:
                line = clean_line(line)                
                city = City.objects.filter(code=line[0]).first()
                if city:
                    hotel, created = Hotel.objects.update_or_create(city=city, code=line[1], defaults={"name": line[2]})   
                    if created:
                        created_hotels += 1
                    else:
                        updated_hotels += 1
                else:
                    errors += 1
            except IntegrityError as e:
                errors += 1
                print(f"Integrity error for line {line}: {str(e)}")
            except Exception as e:
                errors += 1
                print(f"Error processing line {line}: {str(e)}")

        stats = {
            "total_hotels": total_hotels,
            "created_hotels": created_hotels,
            "updated_hotels": updated_hotels,
            "errors": errors,
        }

        return True, stats

    except requests.RequestException as e:
        return False, {
            "error_code": 2,
            "message": f"Errore durante la richiesta API: {str(e)}",
        }
    except Exception as e:
        return False, {
            "error_code": 3,
            "message": f"Errore durante l'importazione: {str(e)}",
        }