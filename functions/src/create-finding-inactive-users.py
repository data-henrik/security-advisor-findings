import json,sys,os, requests

finding={
    "note_name": "",
    "kind": "FINDING",
    "message": "Non-active users have account access",
    "provider_id": "",
    "id": "inactiveUsers",
    "context": {
        "region": "us-south",
        "resource_name": "Account user management",
        "service_name": "IAM"
    },
    "finding": {
        "severity": "HIGH"
    }
}


def main(args):
    response={}
    if len(args["users"])>0:
        headers = { "Authorization" : "Bearer "+args["access_token"], "Content-Type" : "application/json",
                    "accept": "application/json",  "Replace-If-Exists":"true" }
        finding["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/inactiveUsers"
        finding["provider_id"]=args["config"]["provider_id"]
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences"
        response  = requests.post(url, headers=headers, json=finding).json()
    return {"response":response, "finding":finding, "url":url}


if __name__ == "__main__":
    main(json.loads(sys.argv[1]))