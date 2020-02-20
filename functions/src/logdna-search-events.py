# (C) 2020 IBM Corporation
#
# IBM Cloud Functions / OpenWhisk action to scan LogDNA
# entries with the specified query strings.
#
# It is possible to specify multiple query entries and LogDNA
# instances. The results are merged and reported back as a single list.
# A LogDNA API key for the export API is needed to perform the search.

import json,sys,requests
from datetime import datetime

# perform the actual search
def getLogs(region, key, numHours, query):
    url     = "https://api."+region+".logging.cloud.ibm.com/v1/export"
    params = {
        "from": datetime.timestamp(datetime.now())-(3600*int(numHours)),
        "to": datetime.timestamp(datetime.now()),
        "query": query,
        "size": "10000"
        }
    response  = requests.get( url, auth=(key,''), params=params)
    # the result are lines of JSON, so store them individually
    result = [json.loads(jline) for jline in response.text.splitlines()]
    return result

def main(args):
    allLogs=[]
    AT=args["config"]["AT"]
    for config in AT:
        logs=getLogs(config["region"],
                     config["key"],
                     config["numHours"],
                     config["query"])
        allLogs.extend(logs)
    return {"logs":allLogs, "access_token":args["access_token"], "config":args["config"]}

if __name__ == "__main__":
    main(json.loads(sys.argv[1]))