import json,sys,os, requests


finding={
    "note_name": "",
    "kind": "FINDING",
    "message": "LogDNA finding",
    "provider_id": "",
    "id": "logdna",
    "context": {
        "region": "us-south",
        "resource_name": "Activity Tracking",
        "service_name": "LogDNA"
    },
    "finding": {
        "severity": "MEDIUM"
    }
}

kpi={
    "note_name": "",
    "kind": "KPI",
    "message": "External users have account access",
    "provider_id": "",
    "id": "logdnaKPI",
    "context": {
        "region": "us-south",
        "resource_name": "Activity Tracking",
        "service_name": "LogDNA"
    },
    "kpi": {
        "value": 0,
        "total":0
    }
}

def main(args):
    response={}
    kpiResponse={}
    if len(args["logs"])>0:
        headers = { "Authorization" : "Bearer "+args["access_token"], "Content-Type" : "application/json",
                    "accept": "application/json",  "Replace-If-Exists":"true" }
        # Finding
        finding["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/logdna"
        finding["provider_id"]=args["config"]["provider_id"]
        url=args["config"]["host"]+"/v1/"+args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/occurrences"
        response  = requests.post(url, headers=headers, json=finding).json()

        # KPI
        kpi["note_name"]=args["config"]["account_id"]+"/providers/"+args["config"]["provider_id"]+"/notes/logdnaKPI"
        kpi["provider_id"]=args["config"]["provider_id"]
        kpi["kpi"]["value"]=len(args["logs"])
        kpi["kpi"]["total"]=len(args["logs"])
        kpiResponse  = requests.post(url, headers=headers, json=kpi).json()
    return {"findingResponse":response, "kpiResponse":kpiResponse}


if __name__ == "__main__":
    main(json.loads(sys.argv[1]))