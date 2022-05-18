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
psql trivia < trivia.psql
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

Authentication 

# Email: fieldtech@email.com Pass: Fieldtestpass123
# Email: leadtech@email.com Pass: Leadtestpass123
# Email: seniortech@email.com Pass: Seniortestpass123



## Testing

To deploy the tests, run

```bash
dropdb repairshop_test
createdb repairshop_test
psql repairshop_test < repairshop.psql
python test_app.py
```