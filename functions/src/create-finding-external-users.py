# (C) 2020 IBM Corporation
#
# Requests are based on:
# https://cloud.ibm.com/apidocs/security-advisor/findings

import json,sys,requests


finding={
    "note_name": "",
    "kind": "FINDING",
    "message": "External users have account access",
    "provider_id": "",
    "id": "externalUsers",
    "context": {
        "region": "us-south",
        "resource_name": "Account user management",
        "service_name": "IAM"
    },
    "finding": {
        "severity": "HIGH"
    }
}

kpi={
    "note_name": "",
    "kind": "KPI",
    "message": "External users have account access",
    "provider_id": "",
    "id": "externalUsersKPI",
    "context": {
        "region": "us-south",
        "resource_name": "Account user management",
        "service_name": "IAM"
    },
    "kpi": {
        "value": 0,
        "total":0
    }
}

def main(args):
    response={}
    # check if there were external users found
    if len(args["users"])>0:
        # if yes, fill the structures
        headers = { "Authorization" : "Bearer "+args["access_token"], "Content-Type" : "application/json",
                    "accept": "application/json",  "Replace-If-Exists":"true" }
        # Finding
        finding["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/externalUsers"
        finding["provider_id"]=args["config"]["provider_id"]
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences"
        # and send the request
        response  = requests.post(url, headers=headers, json=finding).json()

        # KPI
        kpi["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/externalUsersKPI"
        kpi["provider_id"]=args["config"]["provider_id"]
        kpi["kpi"]["value"]=len(args["users"])
        kpi["kpi"]["total"]=len(args["users"])
        kpiResponse  = requests.post(url, headers=headers, json=kpi).json()
    else:
        # if there are no issues detected, we try to delete possibly existing occurrences
        headers = { "Authorization" : "Bearer "+args["access_token"]}
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences/externalUsers"
        response  = requests.delete(url, headers=headers).json()

        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences/externalUsersKPI"
        kpiResponse  = requests.delete(url, headers=headers).json()

    return {"findingResponse":response, "kpiResponse":kpiResponse}


if __name__ == "__main__":
    main(json.loads(sys.argv[1]))