import json,sys,os, requests


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
    if len(args["users"])>0:
        headers = { "Authorization" : "Bearer "+args["access_token"], "Content-Type" : "application/json",
                    "accept": "application/json",  "Replace-If-Exists":"true" }
        # Finding
        finding["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/externalUsers"
        finding["provider_id"]=args["config"]["provider_id"]
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences"
        response  = requests.post(url, headers=headers, json=finding).json()

        # KPI
        kpi["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/externalUsersKPI"
        kpi["provider_id"]=args["config"]["provider_id"]
        kpi["kpi"]["value"]=len(args["users"])
        kpi["kpi"]["total"]=len(args["users"])
        kpiResponse  = requests.post(url, headers=headers, json=kpi).json()
    return {"findingResponse":response, "kpiResponse":kpiResponse, "finding":finding, "url":url}


if __name__ == "__main__":
    main(json.loads(sys.argv[1]))