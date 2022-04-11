import json
import os
import urllib3

import boto3

class Utils:

    def __init__(self):

        self.awsDeployRegion = str(os.environ.get("awsDeployRegion"))

        self.ssmClient = boto3.client('ssm', region_name=self.awsDeployRegion)

        self.c1asSecurityGroupName = str(os.environ.get("c1asSecurityGroupName"))
        self.c1asApiAuthToken = str(os.environ.get("c1asApiAuthToken"))

        if "ssm:" in self.c1asApiAuthToken:
            ssmParamKey = self.c1asApiAuthToken.split('ssm:')[1]
            if self.getAwsSsmParameter(ssmParamKey):
                self.c1asApiAuthToken = self.getAwsSsmParameter(ssmParamKey)

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

    # Retrieve SSM Parameter value based on parameter key passed.
    def getAwsSsmParameter(self, paramKey):
        
        print("Fetching SSM Parameter value from AWS...")  
        parameter = self.ssmClient.get_parameter(Name=paramKey, WithDecryption=True)

        return parameter ['Parameter']['Value']

    # Store SSM Parameter key and value on the AWS backend for future use.
    def setAwsSsmParameter(self, paramKey, paramValue):        
        
        parameter = self.ssmClient.put_parameter(Name=paramKey, Value=paramValue, Type='String', Overwrite=True)

        print(str(parameter))