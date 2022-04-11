import json
import os
import urllib3

class Utils:

    def __init__(self):

        self.c1asSecurityGroupName = str(os.environ.get("c1asSecurityGroupName"))
        self.c1asApiAuthToken = str(os.environ.get("c1asApiAuthToken"))

        self.httpHeaders = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'ApiKey ' + self.c1asApiAuthToken,
            'api-version': 'v1'
        }

        self.httpObj = urllib3.PoolManager(headers=self.httpHeaders)
        self.c1TrendRegion = self.getApiKeyRegion(self.httpObj)
        self.baseUrl = self.c1asApiEndpointBaseUrl(self.c1TrendRegion)

    # Returns Cloud One region-based Accounts API Endpoint URL.
    def c1AccountsApiEndpointBaseUrl(self):

        return "https://accounts.cloudone.trendmicro.com/api"

    # Retrieve API Key ID from the raw API Key passed to this function.
    def parseApiKeyForKeyId(self):        

        return str(self.c1asApiAuthToken.split(':')[0])

    # Get Cloud One API Region endpoint.
    def getApiKeyRegion(self, http):    

        r = http.request('GET', self.c1AccountsApiEndpointBaseUrl() + '/apikeys/' + self.parseApiKeyForKeyId())

        return json.loads(r.data)["urn"].split(":")[3]

    # Returns Cloud One region-based Services API Endpoint URL.
    def c1asApiEndpointBaseUrl(self, c1TrendRegion):

        return "https://application." + str(c1TrendRegion) + ".cloudone.trendmicro.com"

    # Returns true when request status is success.
    def isHttpRequestSuccess(self, statusCode):

        if statusCode == 204:
            return True
        elif statusCode == 409:
            raise Exception("Error 409: Failure to validate rule(s).")
        elif statusCode == 422:
            raise Exception("Error 422: Unprocessable Entity.")
        return False