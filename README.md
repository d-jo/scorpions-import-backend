# Structure
`./old` - Old code that needs to be migrated to new structure

`./webapi` - Root folder of our API                         

`./webapi/files` - Contains blueprints for uploading and saving files

`./webapi/reports` - Contains blueprints for viewing and managing reports



# Executing the code
Running the testing file upload server

First, you need to set the FLASK_APP environment variable 

(Linux): `export FLASK_APP=scorpions_backend`

(Windows): `set FLASK_APP=scorpions_backend.py`

Then you can run the app with:

`flask run`

To run the sample document parsing code, you can run the file `document_parsing.py` with 

`python document_parsing.py`

# Release Notes

2021-10-05 Release
- Basic document parsing
- Basic file uploading
- Basic file information endpoints