import json
from utils import Utils

class Policies:

    apiCredsKey = apiCredsSecret = None
    groupId = None

    utilsObj = None

    def __init__(self):

        self.utilsObj = Utils()

    def getIllegalFileAccessPolicy(self, groupId):       

        r = self.utilsObj.httpObj.request('GET', self.utilsObj.baseUrl + '/security/file_access/' + groupId + '/policy')        
                
        return json.loads(r.data)

    def addIllegalFileAccessPolicy(self, groupId, existingPolicyDict):

        newRuleDict = {     
            'action': 'allow',
            'glob': '/proc/meminfo'
        }

        existingPolicyDict["read_control"]["configuration"]["rules"].append(newRuleDict)

        print(str(existingPolicyDict))

        r = self.utilsObj.httpObj.request('PUT', self.utilsObj.baseUrl + '/security/file_access/' + groupId + '/policy', body=json.dumps(existingPolicyDict))
                
        return self.utilsObj.isHttpRequestSuccess(r.status)

    def getRCEPolicy(self, groupId):       

        r = self.utilsObj.httpObj.request('GET', self.utilsObj.baseUrl + '/security/rce/' + groupId + '/policy')
                
        return json.loads(r.data)

    def addRCEPolicy(self, groupId, existingPolicyDict):

        newRuleDict = {            
            'action': 'allow',
            'command': '^file.*'
        }

        existingPolicyDict["exec_control"]["configuration"]["rules"].append(newRuleDict)

        print(str(existingPolicyDict))

        r = self.utilsObj.httpObj.request('PUT', self.utilsObj.baseUrl + '/security/rce/' + groupId + '/policy', body=json.dumps(existingPolicyDict))
                
        return self.utilsObj.isHttpRequestSuccess(r.status)