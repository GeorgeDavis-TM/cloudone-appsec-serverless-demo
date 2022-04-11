import json
from utils import Utils

class Groups:

    utilsObj = None

    def __init__(self):

        self.utilsObj = Utils()

    def createNewGroup(self):

        body = {
            "name": "CloudOneServerlessDemo-MgmtApis"
        }        

        r = self.utilsObj.httpObj.request('POST', self.utilsObj.baseUrl + '/accounts/groups', body=json.dumps(body))
        
        jsonResponse = json.loads(r.data)
        # print(str(jsonResponse))

        return {
            "groupId": jsonResponse["group_id"],
            "apiCredsKey": jsonResponse["credentials"]["key"],
            "apiCredsSecret": jsonResponse["credentials"]["secret"]
        }        

    def setGroupEnablePolicy(self, groupId):

        body = {
            'credential_stuffing': 'mitigate',
            'file_access': 'mitigate',
            'ip_protection': 'mitigate',
            'malicious_file_upload': 'mitigate',
            'malicious_payload': 'mitigate',
            'rce': 'mitigate',
            'redirect': 'mitigate',
            'sqli': 'mitigate'
        }

        r = self.utilsObj.httpObj.request('PUT', self.utilsObj.baseUrl + '/accounts/groups/' + str(groupId) + '/settings', body=json.dumps(body))

        return self.utilsObj.isHttpRequestSuccess(r.status)