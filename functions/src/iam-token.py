# Use the Cloud Functions API key to request a Bearer token
import json,sys,os,requests

def getAuthTokens(api_key):
    url     = os.environ.get('__OW_IAM_API_URL')
    headers = { "Content-Type" : "application/x-www-form-urlencoded" }
    data    = "apikey=" + api_key + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response  = requests.post( url, headers=headers, data=data )
    return response.json()

def main(args):
    authTokens = getAuthTokens(os.environ.get('__OW_IAM_NAMESPACE_API_KEY'))

    return {"access_token":authTokens["access_token"],
            "config": args}

if __name__ == "__main__":
    main(json.loads(sys.argv[1]))