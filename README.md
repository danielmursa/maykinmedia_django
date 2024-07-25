# Hotels Maykinmedia Django

## Overview
This Django project includes models for managing cities and hotels. 
The `City` model stores information about cities, and the `Hotel` model stores information about hotels, with each hotel being associated with a specific city.

- **City**: Represents a city with a unique code and name.
- **Hotel**: Represents a hotel with a unique code, name, and a reference to the city it is situated in.

## Project

## Structure Project
<b>maykinmedia_django/</b><br> 
├── <b>hotel/                </b># Main application folder<br> 
&nbsp;&nbsp;&nbsp;    ├── api/<br> 
&nbsp;&nbsp;&nbsp;    ├── management/<br> 
&nbsp;&nbsp;&nbsp;    ├── migrations/<br> 
&nbsp;&nbsp;&nbsp;    ├── templates/<br> 
&nbsp;&nbsp;&nbsp;    ├── admin.py<br> 
&nbsp;&nbsp;&nbsp;    ├── apps.py<br> 
&nbsp;&nbsp;&nbsp;    ├── forms.py<br> 
&nbsp;&nbsp;&nbsp;    ├── models.py<br> 
&nbsp;&nbsp;&nbsp;    ├── settings.py<br> 
&nbsp;&nbsp;&nbsp;    ├── tests.py<br> 
&nbsp;&nbsp;&nbsp;    ├── urls.py<br> 
&nbsp;&nbsp;&nbsp;    ├── utils.py<br> 
&nbsp;&nbsp;&nbsp;    ├── views.p<br> 
├── <b>maykinmedia_django/                </b># Base application configurations<br> 
&nbsp;&nbsp;&nbsp;    ├── settings.py<br> 
&nbsp;&nbsp;&nbsp;    ├── urls.py<br> 
&nbsp;&nbsp;&nbsp;    ├── asgi.py<br> 
&nbsp;&nbsp;&nbsp;    ├── wsgi.py<br> 
├── gitingore             <br> 
├── docker-compose.yml             <br> 
├── Dockerfile             <br> 
├── entrypoint.sh           <br> 
├── manage.py           <br> 
├── maykinmedia_logger.log           <br> 
├── requirements.txt           <br> 
└── readme.md          <br> 


## Features

- **City Management**: 
  - Define and manage cities with unique codes and names. Each city entry includes a code (e.g., AMS) and a name (e.g., Amsterdam).
  
- **Hotel Management**:
  - Define and manage hotels associated with cities. Each hotel entry includes a unique code (e.g., AMS01), a name (e.g., Ibis Amsterdam Airport), and a foreign key linking it to a city.

- **Django Admin Integration**:
  - Manage cities and hotels through the Django Admin interface. You can add, edit, or delete entries for cities and hotels using a user-friendly web interface.

- **Daily Import Logic**:
  - **Automated Data Import**: Automatically import city and hotel data from external sources (API) on a daily basis.
    
  - **Scheduling Imports**: The daily import process can be scheduled using cron jobs or task schedulers like Celery. 
    ```bash
    cat crontab_backup.txt    
    ```
  
  - **Error Handling and Logging**: Includes mechanisms to handle errors during the import process and log issues for troubleshooting. This helps in maintaining data integrity and identifying potential problems.

  ```bash
    python manage.py import_cities
    python manage.py import_hotels
    
    # Output success --> Import successful: {'total_cities': n, 'created_cities': n, 'updated_cities': n, 'errors': n}
  ```

- **Dynamic City and Hotel Viewing**:
  - **City Selection**: Create a view and template that allows users to choose a city from a list populated with cities from the dataset.
  
  - **Hotel Listing**: Display all hotels located in the selected city. 

- **Unit Testing**:
  - **Quality Assurance**: Add unit tests to ensure the quality and reliability of your code. 
  
  ```bash
    python manage.py test
  ```

- **Interactive City and Hotel JS Async**:
  - **Asynchronous Data Fetching**: Utilize JavaScript to perform asynchronous requests to retrieve hotel data based on the selected city. The hotel list will automatically update without requiring a page reload, providing a seamless and interactive experience.

  - **Dynamic Hotel Display**: Automatically display a list of hotels corresponding to the selected city. This feature ensures that users receive immediate feedback and can see relevant hotel options as soon as a city is selected.

- **API Integration**: Create RESTful APIs to expose city and hotel data. These APIs will be used by the front-end to dynamically fetch and display data.

- **Containerized Deployment**: 
    - **Docker Containers**: Create Docker containers for the Django application and database. This simplifies the deployment process by ensuring consistent environments across different stages (development, testing, production).


## Installation

### Clone the Repository

```bash
    git clone https://github.com/danielmursa/maykinmedia_django
    cd maykinmedia_django
```

### Setup

#### Build and Run with Docker Compose

1. **Build and Start the Containers**

   ```bash
   docker-compose build
   ```
    ```bash
   docker-compose up
   ```
   The Django application will be available at `http://127.0.0.1:8000/`.
   ```bash
   docker ps # to view all containers, select maykinmedia_django_web_1

   docker exec -it maykinmedia_django_web_1 bash
   
   python manage.py import_cities
   
   python manage.py import_hotels
   ```
   Populate Data

## Usage

### Django Admin

To manage cities and hotels, log in to the Django Admin interface:

- URL: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials: 
    ```bash
    username: admin
    password: admin
   ```

### Models

#### City Model

- **code**: CharField, unique code for the city
- **name**: CharField, name of the city

#### Hotel Model

- **city**: ForeignKey to the City model, indicates the city where the hotel is located
- **code**: CharField, unique code for the hotel
- **name**: CharField, name of the hotel

## Contact

For any questions or issues, please contact [danielmursa99@gmail.com](mailto:danielmursa99@gmail.com).