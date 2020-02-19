import json,sys,os, requests


def getUsers(iam_token, account_id):
    url = 'https://user-management.cloud.ibm.com/v2/accounts/'+account_id+'/users'
    headers = { "Authorization" : "Bearer "+iam_token }
    response = requests.get(url, headers=headers)
    return response.json()


def main(args):
    users=getUsers(args["access_token"], args["config"]["account_id"])

    result={
            "access_token":args["access_token"],
            "config":args["config"],
            "inactiveUsers":[]
            }
    
    for user in users["resources"]:
        if user["state"] != "ACTIVE":
            result["inactiveUsers"].append(user)
    
    return result

if __name__ == "__main__":
    main(json.loads(sys.argv[1]))