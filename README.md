# Structure
`./old` - Old code that needs to be migrated to new structure

`./webapi` - Root folder of our API                         

`./webapi/files` - Contains blueprints for uploading and saving files

`./webapi/reports` - Contains blueprints for viewing and managing reports



# Executing the code
`cd` into the `webapi` folder, then you can run the app with:

`flask run`

To run the sample document parsing code, you can run the file `webapi/files/document_parsing.py` with 

`python document_parsing.py`

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