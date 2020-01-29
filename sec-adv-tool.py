import json, argparse, importlib, requests
from os.path import join, dirname
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time
import ibm_security_advisor_findings_api_client
from ibm_security_advisor_findings_api_client.rest import ApiException
from ibm_cloud_sdk_core import IAMTokenManager, ApiException
from pprint import pprint

import random
import string

configSecAdv={
    "authToken":None
}

def loadAndInit(confFile=None):
    # Credentials are read from a file
    with open(confFile) as confFile:
        configSecAdv.update(json.load(confFile))

    # Initialize the Watson Assistant client, use API V2
    if 'apikey' in configSecAdv:
        # Authentication via IAM
        token_manager = IAMTokenManager("zvvErrJfqb9s15qFQq8OzjhCJka5q3DSwhVirDznqfW-")

        configSecAdv["authToken"] = 'Bearer '+token_manager.request_token()['access_token']
    else:
        print('Expected apikey in credentials.')
        exit


# Define parameters that we want to catch and some basic command help
def initParser(args=None):
    parser = argparse.ArgumentParser(description='Manage findings for IBM Cloud Security Advisor',
                                     prog='sec-adv-tool.py',
                                     usage='%(prog)s [-h | -interactive | -findings ] [options]')
    parser.add_argument("-interactive",dest='interactive', action='store_true', help='interactive mode')
    parser.add_argument("-findings",dest='findings', action='store_true', help='search findings')
    parser.add_argument("-config",dest='confFile', default='config.json', help='configuration file')

    return parser

def ListProviders():
    headers = { "Authorization" : configSecAdv["authToken"], "Content-Type" : "application/json" }
    response  = requests.get( configSecAdv["host"]+"/v1/"+configSecAdv["account_id"]+"/providers/", headers=headers )
    pprint (response.json())

def findingsByProvider():
    provinput = input("Please enter the provider ID:\n")
    configuration = ibm_security_advisor_findings_api_client.Configuration()
    configuration.host= "https://us-south.secadvisor.cloud.ibm.com/findings"

    api_findings_instance = ibm_security_advisor_findings_api_client.FindingsNotesApi(ibm_security_advisor_findings_api_client.ApiClient(configuration))
    api_occurrence_instance = ibm_security_advisor_findings_api_client.FindingsOccurrencesApi(ibm_security_advisor_findings_api_client.ApiClient(configuration)) 
    page_size=50
    provider_id=provinput


    try:
        print("Searching occurrences")
        occurrences = api_occurrence_instance.list_occurrences(configSecAdv["account_id"],configSecAdv["authToken"], provider_id, page_size=page_size).occurrences
        pprint(occurrences)

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)

def interactive():
    # Loop to get input
    while True:
        print("(F)indings / (P)rovider / e(X)it")
        # get some input
        minput = input("Please enter your input choice:\n")
        # if we catch a "bye" then exit after deleting the session
        if (minput == "x" or minput == "X"):
            print('Bye...')
            break
        elif (minput == "F"):
            findingsByProvider()
            pass
        elif (minput == "P"):
            ListProviders()
            pass
        else:
            pass



#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    # initialize parser
    parser = initParser()
    parms =  parser.parse_args()
    # enable next line to print parameters
    # print parms

    # load configuration and initialize Watson
    loadAndInit(confFile=parms.confFile)

    if (parms.interactive):
        interactive()
    elif (parms.findings):
        findingsByProvider()
    else:
        parser.print_usage()