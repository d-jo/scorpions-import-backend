import os, requests, pytest
import json
from auth.auth import requires_auth, get_token_auth_header
from users.users import user_info
baseUrl = 'http://localhost:5000'
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFPZ3FZOUlCMkZuQ2d3NnVIMGNQbiJ9.eyJpc3MiOiJodHRwczovL2Rldi16LW5xYThzMC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDY4Mzc2NDY5OTE3NzQxNjc1NzgiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtei1ucWE4czAudXMuYXV0aDAuY29tL2FwaS92Mi8iLCJodHRwczovL2Rldi16LW5xYThzMC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjM4ODUxODAzLCJleHAiOjE2Mzk0NTY2MDMsImF6cCI6IlU2VldnVE1QVU1mTThTYVF1QWhqSXhLdVl5b3BEQjMxIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCJ9.FHZgTMetfuGWBiczIbQI2tm-xgs3SyFiJfu96DBj44K7msN0_HNr40PfivDn9mFg-KyB7owBek8fPDvxZuAQItoTGK54uzChICbq4ewV9dMJnr1lW2HNKVtramxwJM15sEwvojye7S2eaKnYVN1WvPBvjwWWrooCLub5tqpT-RczO8nCcIM6F2yHeyuXyrYz_F_PszoqiRyFW577jYM8o8WW_rTtDqAvd0W2dyOPC5_6RZsUeE6PbSB7DcXcC14udjEtsvA_VxJdrgNEQuXic6peYKjYjXZ4PUqCXJd52Bi5xKs11Z-at5hiL8DdNPIURLI36L_PS6hPqF1amYk34A'
def test_dashboard(): 
   response = requests.get(baseUrl + '/dashboard/', headers= {'Authorization': 'Bearer ' + token})
   assert response.status_code == 200


def test_files_view():
    response = requests.get(baseUrl + '/view/0', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200

def test_files_audit():
    response = requests.get(baseUrl + '/audit/file/0', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_report_statistics():
    response = requests.get(baseUrl + '/statistics', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_report_trigger_process():
    response = requests.get(baseUrl + '/reports/extract_data', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_report_edit():
    response = requests.post(baseUrl + '/reports/12/edit', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


@pytest.mark.skip(reason="This test will pass, but it isn't actually sending the\
form data correctly.")
def test_upload_file():
    file = 'endpoint_test_file.txt'
    firname = os.path.join('./data', file)
    # print(os.getcwd())
    # print(firname)
    f = open(firname, 'rb')
    # print(f.read())
    data = {
        'file': ([f])
    }
    # print(data)
    response = requests.post(baseUrl + '/files', data=data)
    # print(response.text)
    assert response.status_code == 200


