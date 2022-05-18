# Udacity Full Stack Network Developer Capstone

## Goal

The goal of this project is to produce an API that makes use of Auth0 authorization, SQLAlchemy + PostgreSQL database, Python + Flask, and Heroku to create an application that combines the knownledge we have gained over the entirety of this course. [Live on Heroku](https://fscapstoneprj.herokuapp.com/)

## Getting Started

### Install Dependencies

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Navigate to the root (`fscapstone/`) of the project directory and run:

```bash
pip install -r requirements.txt
```
### Set up the Database

With Postgres running, create a `repairshop` database:

```bash
createbd repairshop
```

Populate the database using the `repairshop.psql` file provided. From the `fscapstone` folder in terminal run:

```bash
psql repairshop < repairshop.psql
```

### Run the Server

From within the `fscapstone` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Authentication

Authentication is done through the `/login` endpoint which will redirect the user to the formatted authentication url, where the user can then input one of the following credentials for the proper authentication. The user will then be redirected back to the `/` endpoint and their token will be contained in the URL. This can then be used within curl to access the rest of the endpoints with authorization e.g. `curl --request GET 'http://localhost:5000/seniortechs' -H "Authorization: Bearer ${TOKEN}" | jq .`

- Email: fieldtech@email.com Pass: Fieldtechpass123
- Email: leadtech@email.com Pass: Leadtechpass123
- Email: seniortech@email.com Pass: Seniortechpass123

## Testing

To deploy the tests, run

```bash
dropdb repairshop_test
createdb repairshop_test
psql repairshop_test < repairshop.psql
python test_app.py
```

## API Endpoint Documentation

`GET '/api/fieldtechs'`

- Fetches a dictionary of fieldtechs in which the keys are the ids, names, and employeeIDs and the value is the corresponding string/int
- Request Arguments: Auth Token ('get:fieldtech')
- Returns: An object with a single key, `fieldtechs`, that contains an object of `id: INT, name: STRING, employeeID: INT` key: value pairs.

```json
{
    "fieldtechs": [
        {
            "employeeID": 233412,
            "id": 1,
            "name": "Bob"
        },
        {
            "employeeID": 233443,
            "id": 2,
            "name": "Greg"
        }
    ],
    "success": true
}
```

`GET '/api/leadtechs'`

- Fetches a dictionary of leadtechs in which the keys are the ids, names, employeeIDs, and fieldtech_ids and the value is the corresponding string/int
- Request Arguments: Auth Token ('get:leadtech')
- Returns: An object with a single key, `leadtechs`, that contains an object of `id: INT, name: STRING, employeeID: INT, fieldtech_ids: INT` key: value pairs.

```json
{
    "leadtechs": [
        {
            "employeeID": 233123,
            "id": 1,
            "name": "Polea",
            "fieldtech_ids": 1
        },
        {
            "employeeID": 233565,
            "id": 2,
            "name": "Luther",
            "fieldtech_ids": 1
        }
    ],
    "success": true
}
```

`GET '/api/seniortechs'`

- Fetches a dictionary of seniortechs in which the keys are the ids, names, employeeIDs, fieldtech_ids, and leadtech_ids and the value is the corresponding string/int
- Request Arguments: Auth Token ('get:seniortech')
- Returns: An object with a single key, `fieldtechs`, that contains an object of `id: INT, name: STRING, employeeID: INT, fieldtech_ids: INT, leadtech_ids: INT` key: value pairs.

```json
{
    "fieldtechs": [
        {
            "employeeID": 000123,
            "id": 1,
            "name": "Roark",
            "fieldtech_ids": 1,
            "leadtech_ids": 2
        },
    ],
    "success": true
}
```

`POST '/api/fieldtechs'`

- Creates a new fieldtech object using a json object containing the name and employeeID key:value pairs
- Request Arguments: Auth Token ('post:fieldtech')
- Returns: An object containing a list of  `fieldtechs`, that contain an object of `id: INT, name: STRING, employeeID: INT` key: value pairs, and `success`

`POST '/api/leadtechs'`

- Creates a new leadtech object using a json object containing the name, employeeID, fieldtech_ids key:value pairs
- Request Arguments: Auth Token ('post:leadtech')
- Returns: An object containing a list of  `leadtechs`, that contain an object of `id: INT, name: STRING, employeeID: INT, fieldtech_ids: INT` key: value pairs, and `success`

`PATCH '/api/fieldtechs/<int:id>'`

- Updates an existing fieldtech object using a json object optionally containing the name and employeeID key:value pairs and the fieldTech.id
- Request Arguments: Auth Token ('patch:fieldtech'), fieldTech.id
- Returns: An object containing a list of  `fieldtechs`, that contain an object of `id: INT, name: STRING, employeeID: INT` key: value pairs, and `success`

`PATCH '/api/leadtechs/<int:id>'`

- Updates an existing leadtech object using a json object containing the name, employeeID, and fieldtech_ids key:value pairs and the leadTech.id
- Request Arguments: Auth Token ('patch:leadtech'), leadTech.id
- Returns: An object containing a list of  `leadtechs`, that contain an object of `id: INT, name: STRING, employeeID: INT, fieldtech_ids: INT` key: value pairs, and `success`

`DELETE '/api/fieldtechs/<int:id>'`

- Deletes an existing fieldtech object using the fieldTech.id
- Request Arguments: Auth Token ('delete:fieldtech'), fieldTech.id
- Returns: An object containing `success` and the `deleted: id`

`DELETE '/api/leadtechs/<int:id>'`

- Deletes an existing leadtech object using the leadTech.id
- Request Arguments: Auth Token ('delete:leadtech'), leadTech.id
- Returns: An object containing `success` and the `deleted: id`
