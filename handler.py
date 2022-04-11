import trend_app_protect.start
import json
import logging
import time
import os

import boto3

from groups import Groups
from policies import Policies
from utils import Utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Store SSM Parameter key and value on the AWS backend for future use.
def setAWSSSMParameter(awsRegion, paramKey, paramValue):

    ssmClient = boto3.client('ssm', region_name=awsRegion)
    
    parameter = ssmClient.put_parameter(Name=paramKey, Value=paramValue, Type='String', Overwrite=True)

    print(str(parameter))

def main(event, context):

    awsDeployRegion = str(os.environ.get("awsDeployRegion"))
    
    groupsObj = Groups()

    createGroupResponse = groupsObj.createNewGroup()
    # print(str(createGroupResponse))

    setAWSSSMParameter(awsDeployRegion, "TREND_AP_KEY", createGroupResponse["apiCredsKey"])
    setAWSSSMParameter(awsDeployRegion, "TREND_AP_SECRET", createGroupResponse["apiCredsSecret"])

    time.sleep(5)

    groupsObj.setGroupEnablePolicy(createGroupResponse["groupId"])

    policyObj = Policies()

    currentIllegalFileAccessPolicyDict = policyObj.getIllegalFileAccessPolicy(createGroupResponse["groupId"])
    currentRCEPolicyDict = policyObj.getRCEPolicy(createGroupResponse["groupId"])

    policyObj.addIllegalFileAccessPolicy(createGroupResponse["groupId"], currentIllegalFileAccessPolicyDict)
    policyObj.addRCEPolicy(createGroupResponse["groupId"], currentRCEPolicyDict)

    print(str(policyObj.getIllegalFileAccessPolicy(createGroupResponse["groupId"])))
    print(str(policyObj.getRCEPolicy(createGroupResponse["groupId"])))

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
