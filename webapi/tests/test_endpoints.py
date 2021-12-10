import os, requests, pytest
import json
from auth.auth import requires_auth, get_token_auth_header
from users.users import user_info
baseUrl = 'http://localhost:5000'
# !!! Give a valid token with the AAC role before running this test !!!
token = ''


def test_upload_file():
    file = 'endpoint_word_doc.docx'
    firname = os.path.join('./data', file)
    f = open(firname, 'rb')
    data = {
        'file': (f)
    }
    response = requests.post(baseUrl + '/files/', files=data, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_dashboard(): 
   response = requests.get(baseUrl + '/dashboard/', headers= {'Authorization': 'Bearer ' + token})
   assert response.status_code == 200
   resp = response.json()
   assert 'endpoint_word_doc.docx' in resp['uploaded']


def test_report_trigger_process():
    files = ['endpoint_word_doc.docx']
    response = requests.post(baseUrl + '/reports/extract_data', headers={'Authorization': 'Bearer ' + token}, json=files)
    assert response.status_code == 200


def test_search():
    search_key = {
        'search_key': 'AAC Import'
    }
    response = requests.post(baseUrl + '/reports/search', headers={'Authorization': 'Bearer ' + token}, json=search_key)
    assert response.status_code == 200
    resp = response.json()
    assert resp['review'] is not None


def test_files_view():
    # Get id of test file for view endpoint.
    search_key = {
        'search_key': 'AAC Import'
    }
    fileId = ''
    response = requests.post(baseUrl + '/reports/search', headers={'Authorization': 'Bearer ' + token}, json=search_key)
    resp = response.json()
    for file in resp['review']:
        if file[1] == 'AAC Import':
            fileId = str(file[0])
            break
    response = requests.get(baseUrl + '/reports/' + fileId, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    resp = response.json()
    assert len(resp['slos']) == 0


def test_files_audit():
    search_key = {
        'search_key': 'AAC Import'
    }
    fileId = '0'
    response = requests.post(baseUrl + '/reports/search', headers={'Authorization': 'Bearer ' + token}, json=search_key)
    resp = response.json()
    for file in resp['review']:
        if file[1] == 'AAC Import':
            fileId = str(file[0])
            break

    response = requests.get(baseUrl + '/audit/file/' + fileId, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    resp = response.json()
    assert resp['audit_trail'] is not None


def test_report_statistics():
    response = requests.get(baseUrl + '/statistics', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_report_edit():
    search_key = {
        'search_key': 'AAC Import'
    }
    fileId = '0'
    response = requests.post(baseUrl + '/reports/search', headers={'Authorization': 'Bearer ' + token}, json=search_key)
    resp = response.json()
    for file in resp['review']:
        if file[1] == 'AAC Import':
            fileId = str(file[0])
            break

    response = requests.get(baseUrl + '/reports/' + fileId, headers={'Authorization': 'Bearer ' + token})
    resp = response.json()
    assert len(resp['slos']) == 0

    created = resp['created']
    creator_id = resp['creator_id']

    update_payload = {
        'academic_year': '2021-2022',
        'accreditation_body': None,
        'additional_information': '',
        'author': 'Team Scorpions',
        'college': 'College of IS&T',
        'created': int(created),
        'creator_id': creator_id,
        'date_range': '2021',
        'degree_level': 'BS',
        'department': 'Scorpions',
        'has_been_reviewed': True,
        'id': int(fileId),
        'last_accreditation_review': None,
        'program': 'AAC Import',
        'slos_meet_standards': '',
        'stakeholder_involvement': '',
        'title': 'NON-ACCREDITED PROGRAM',
        'slos': [],
        'valid': True,
        'new_slos': [
                {
                    'accredited_data_analyses': [],
                    'bloom': 'Knowledge',
                    'collection_analyses': [],
                    'common_graduate_program_slo': 'NA',
                    'decision_actions': [],
                    'description': 'This was added from an endpoint test',
                    'id': -1,
                    'measures': [],
                    'methods': [],
                    'report_id': int(fileId),
                }
            ]
    }

    response = requests.post(baseUrl + '/reports/' + fileId, headers={'Authorization': 'Bearer ' + token}, json=update_payload)
    assert response.status_code == 200

    response = requests.get(baseUrl + '/reports/' + fileId, headers={'Authorization': 'Bearer ' + token})
    resp = response.json()
    assert len(resp['slos']) == 1

    response = requests.get(baseUrl + '/dashboard/', headers= {'Authorization': 'Bearer ' + token})
    resp = response.json()
    assert [int(fileId), 'AAC Import', '2021-2022'] in resp['done']


def test_delete_file():
    search_key = {
        'search_key': 'AAC Import'
    }
    fileId = '0'
    response = requests.post(baseUrl + '/reports/search', headers={'Authorization': 'Bearer ' + token}, json=search_key)
    resp = response.json()
    # File should be in done at this point.
    for file in resp['done']:
        if file[1] == 'AAC Import':
            fileId = str(file[0])
            break

    response = requests.delete(baseUrl + '/reports/' + fileId, headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200

    response = requests.get(baseUrl + '/dashboard/', headers= {'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    resp = response.json()
    assert [int(fileId), 'AAC Import', '2021-2022'] not in resp['done']

