## Montenegro IBAN Validation API
#### This is a simple API developed using Django to validate IBANs from Montenegro. It provides two endpoints for IBAN validation and listing the previous IBAN checks.
### Installation
- Clone the repository from GitHub:
    ```
    git clone https://github.com/captaindev109/iban-validator.git
    ```
- Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
- Create database and apply inital migration:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
- Run the Django development server:
    ```
    python manage.py runserver
    ```
python manage.py test validator_api.tests

### Endpoints
**Endpoint for IBAN validation**

- URL: /validate-iban

- Method: POST

- Request parameter:

    * iban (String): The IBAN to validate.
- Response:

     Successful validation: HTTP status code 200 OK with a JSON response:
    ```
    {
        "valid": true
    }
    ```   
    or
    ```
    {
        "valid": false
    }
    ```   

    Faulty request: HTTP status code 400 Bad Request with a JSON error response:
    ```
    {
        "error": "Invalid request. Please check the entered IBAN."
    }
    ```  

**Endpoint for listing the previous IBAN checks**

- URL: /validate-history

- Method: GET

- Response:

    Successful request: HTTP status code 200 OK with a JSON response containing a list of previous IBAN validations:
    ```   
    {
        "history": [
            {
                "iban": "DE89370400440532013000",
                "valid": true,
                "timestamp": "2023-05-15T10:30:00Z"
            },
            {
                "iban": "GB29NWBK60161331926819",
                "valid": false,
                "timestamp": "2023-05-14T15:45:00Z"
            },
            ...
        ]
    }

### Storage Mechanism
This Django app is configured to use a SQLite database. The database settings can be found in the DATABASES variable in the settings.py file.

### Unit Tests
The API includes unit tests for the IBAN validation functions. You can run the tests using the following command:
```
python manage.py test
```