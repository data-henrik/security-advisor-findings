# (C) 2020 IBM Corporation
#
# IBM Cloud Functions / OpenWhisk action to scan for an
# external user within the account users (User Management)
#
# "external" is determined by the configured email_domain
import json,sys,requests

def main(args):
    url     = "https://user-management.cloud.ibm.com/v2/accounts/"+args["config"]["account_id"]+"/users"
    headers = { "Authorization" : args["access_token"], "Content-Type" : "application/json" }
    response  = requests.get( url, headers=headers).json()
    # TODO, handle next_url not NULL => more than 100 users

    result={"users":[]}
    domain=args["config"]["email_domain"]
    domain_len=len(domain)
    for user in response["resources"]:
        if user["email"][-domain_len:] != domain:
            result["users"].append({"email":user["email"],"firstname":user["firstname"]})
    return {"users":result["users"], "access_token":args["access_token"], "config":args["config"]}

if __name__ == "__main__":
    main(json.loads(sys.argv[1]))