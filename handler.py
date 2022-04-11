import trend_app_protect.start
import json
import logging
import time
import os

from groups import Groups
from policies import Policies
from utils import Utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event, context):    
    
    utilsObj = Utils()
    groupsObj = Groups()

    createGroupResponse = groupsObj.createNewGroup()
    # print(str(createGroupResponse))

    utilsObj.setAwsSsmParameter("TREND_AP_KEY", createGroupResponse["apiCredsKey"])
    utilsObj.setAwsSsmParameter("TREND_AP_SECRET", createGroupResponse["apiCredsSecret"])

    time.sleep(5)

    groupsObj.setGroupEnablePolicy(createGroupResponse["groupId"])

    policyObj = Policies()

    currentIllegalFileAccessPolicyDict = policyObj.getIllegalFileAccessPolicy(createGroupResponse["groupId"])
    currentRCEPolicyDict = policyObj.getRCEPolicy(createGroupResponse["groupId"])

    policyObj.addIllegalFileAccessPolicy(createGroupResponse["groupId"], currentIllegalFileAccessPolicyDict)
    policyObj.addRCEPolicy(createGroupResponse["groupId"], currentRCEPolicyDict)

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
