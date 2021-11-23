# Structure
`./old` - Old code that needs to be migrated to new structure

`./webapi` - Root folder of our API                         

`./webapi/files` - Contains blueprints for uploading and saving files

`./webapi/reports` - Contains blueprints for viewing and managing reports

`./webapi/database` - Contains database driver and helper functions



# Executing the code
First, ensure that the `config.json` and `creds.json` files exist in the `webapi` folder. (See Configuration section)

`cd` into the `webapi` folder, then you can run the app with:

`flask run`

To run the sample document parsing code, you can run the file `webapi/files/document_parsing.py` with 

`python document_parsing.py`



# Configuration 
The `config.json` file is included in the repo and set up for development.
Ensure keys are not removed and they can be changed to configure the application.

The `creds.json` file is not included in the version control and contains sensitve configuration data. 

Required `creds.json` keys:

- "db_username" - for the database connection
- "db_password" - for the database connection
- "secret_key" - a secret key flask uses for cross-origin requests
- "AUTH0_DOMAIN" - the domain for verifying auth0 tokens. for us this is the domain for the frontend SPA application
- "API_AUDIENCE" - this is one of the audiences included in the JWT claim. for us it is the domain + /api/v2/ may end up being something else
- "AUTH0_MANAGEMENT_API_URL" - URL for the auth0 management service
- "AUTH0_MANAGEMENT_API_TOKEN" - Auth0 management api JWT



# Release Notes

## 2021-10-05 Release

- Basic document parsing
- Basic file uploading
- Basic file information endpoints

## 2021-10-21 Release

- Start documentation
- Start testing
- Update document processing
- - Now extracts tables and keeps checkbox information paird with cell

## 2021-11-09 Release

- Added first version of Models for representing our objects
- Added the reduced database schema as a base for our tables
- Added stub endpoints
- Added database driver and general functions for interacting with the database
- Added ability to send extracted files to database
- Added endpoint tests to verify http response code

# 2021-11-23 Release

- Added CRUD endpoints 
- Added Admin endpoints
- Added AuditLog functionality (entries created on CRUD operations)
- Updated report schema to support scoped report access for needs review/done reports
- Added roles and authentication (possible roles: aac (admin) and instructor)
- Added Auth0 management API functionality
- Improved report parsing (not hooked up to endpoint yet, will be in MS5)
