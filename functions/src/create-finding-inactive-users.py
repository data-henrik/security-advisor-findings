import json,sys,os, requests

finding={
    "note_name": "accountID/providers/data_henrik/notes/inactiveUsers",
    "kind": "FINDING",
    "message": "Non-active users have account access",
    "provider_id": "data_henrik",
    "id": "",
    "context": {
        "region": "us-south",
        "resource_name": "Account user management",
        "service_name": "IAM"
    },
    "finding": {
        "severity": "HIGH"
    },
    "kpi": {
        "value":0
    }
}


def main(args):
    response={}
    if len(args["users"])>0:
        headers = { "Authorization" : "Bearer "+args["access_token"], "Content-Type" : "application/json",
                    "accept": "application/json",  "Replace-If-Exists":"true" }
        finding["note_name"]=args["config"]["account_id"]+"/providers/data_henrik/notes/inactiveUsers"
        finding["id"]="inactiveUsers"
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/data_henrik/occurrences"
        finding["kpi"]["value"]=len(args["users"])
        data = finding
        response  = requests.post(url, headers=headers, json=data).json()
    return {"response":response, "finding":finding, "url":url}


if __name__ == "__main__":
    main(json.loads(sys.argv[1]))