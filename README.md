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



# Release Notes

2021-10-05 Release
- Basic document parsing
- Basic file uploading
- Basic file information endpoints

2021-10-21 Relase
- Start documentation
- Start testing
- Update document processing
- - Now extracts tables and keeps checkbox information paird with cell