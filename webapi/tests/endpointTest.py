import os, requests, pytest

baseUrl = 'http://localhost:5000'

def test_dashboard():
    response = requests.get(baseUrl + '/dashboard')
    assert response.status_code == 200


def test_files_view():
    response = requests.get(baseUrl + '/view/0')
    assert response.status_code == 200


def test_files_audit():
    response = requests.get(baseUrl + '/audit/file/0')
    assert response.status_code == 200


def test_report_statistics():
    response = requests.get(baseUrl + '/statistics')
    assert response.status_code == 200


def test_report_trigger_process():
    response = requests.get(baseUrl + '/reports/trigger_process')
    assert response.status_code == 200


@pytest.mark.skip(reason="This test will pass, but it isn't actually sending the\
    form data correctly.")
def test_upload_file():
    file = 'endpoint_test_file.txt'
    firname = os.path.join('./data', file)
    print(os.getcwd())
    print(firname)
    f = open(firname, 'rb')
    # print(f.read())
    data = {
        'file': ([f])
    }
    print(data)
    response = requests.post(baseUrl + '/files', data=data)
    print(response.text)
    assert response.status_code == 200


