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

SAConfiguration=None
API_Notes_Instance=None
API_Occurrence_Instance=None

def loadAndInit(confFile=None):
    # Credentials are read from a file
    with open(confFile) as confFile:
        configSecAdv.update(json.load(confFile))

    # Initialize the Watson Assistant client, use API V2
    if 'apikey' in configSecAdv:
        # Authentication via IAM
        token_manager = IAMTokenManager(configSecAdv["apikey"])
        configSecAdv["authToken"] = 'Bearer '+token_manager.request_token()['access_token']
    else:
        print('Expected apikey in credentials.')
        exit
    
    global SAConfiguration
    global API_Notes_Instance
    global API_Occurrence_Instance
    SAConfiguration = ibm_security_advisor_findings_api_client.Configuration()
    SAConfiguration.host= configSecAdv["host"]

    API_Notes_Instance = ibm_security_advisor_findings_api_client.FindingsNotesApi(ibm_security_advisor_findings_api_client.ApiClient(SAConfiguration))
    API_Occurrence_Instance = ibm_security_advisor_findings_api_client.FindingsOccurrencesApi(ibm_security_advisor_findings_api_client.ApiClient(SAConfiguration)) 


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
    page_size=50
    provider_id=provinput


    try:
        print("Searching occurrences")
        occurrences = API_Occurrence_Instance.list_occurrences(configSecAdv["account_id"],configSecAdv["authToken"], provider_id, page_size=page_size).occurrences
        pprint(occurrences)

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)

def notesByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput

    try:
        print("Searching notes")
        notes = API_Notes_Instance.list_notes(configSecAdv["account_id"],configSecAdv["authToken"], provider_id, page_size=page_size).notes
        pprint(notes)

    except ApiException as e:
        print("Exception when calling APIs: %s\n" % e)

def insertOccurrence():
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with findings occurrence to insert:\n")
    
    with open(fileInput) as occFile:
        newOcc=json.load(occFile)
    if newOcc["provider_id"] != provider_id:
        print("Warning: Provider IDs do not match...")

    print("Creating TEST occurrence")
    api_response = API_Occurrence_Instance.create_occurrence(newOcc, configSecAdv["authToken"], configSecAdv["account_id"], provider_id)
    pprint(api_response)
    print("Created TEST occurrence")

def deleteOccurrence():
    provider_id = input("Please enter the provider ID:\n")
    occurrence_id = input("Please enter the occurrence ID:\n")

    api_response = API_Occurrence_Instance.delete_occurrence(configSecAdv["account_id"],configSecAdv["authToken"],provider_id, occurrence_id)
    pprint(api_response)

def interactiveFindings():
    # Loop to get input
    while True:
        print("\nFINDINGS: (L)ist / (I)nsert / (D)elete / (B)ack")
        # get some input
        minput = input("Please enter your input choice:\n")
        # if we catch a "bye" then exit
        if (minput == "B" or minput == "b"):
            break
        elif (minput == "L" or minput == "l"):
            findingsByProvider()
            pass
        elif (minput == "I" or minput == "i"):
            insertOccurrence()
            pass
        elif (minput == "D" or minput == "d"):
            deleteOccurrence()
            pass
        else:
            print("wrong option")
            pass

def interactive():
    # Loop to get input
    while True:
        print("\n(F)indings / (P)roviders / (N)otes / e(X)it")
        # get some input
        minput = input("Please enter your input choice:\n")
        # if we catch a "bye" then exit
        if (minput == "x" or minput == "X"):
            print('Bye...')
            break
        elif (minput == "F" or minput == "f"):
            interactiveFindings()
            pass
        elif (minput == "P" or minput == "p"):
            ListProviders()
            pass
        elif (minput == "N" or minput == "n"):
            notesByProvider()
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