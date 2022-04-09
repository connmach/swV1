import requests
import responses
import pytest
import json

def test_send_aa():
    jsonData={"TaskAction":"getNxtTask","TaskId":"A01_3","userId":"guest","courseId":"A01","moduleId":"M01","status":"progress","progress":'45'}
#    jsonData={'action':'Update'}

    response = requests.post(
        "http://192.46.208.71:5022/ps/api/v1/platformServices/qnRepo/",
        headers={"Content-Type": "application/json"},
        data=json.dumps(jsonData,indent=4)) 
    print(response)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

test_send_aa()