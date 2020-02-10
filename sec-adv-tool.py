import json, argparse, importlib, requests
from os.path import join, dirname
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time
from ibm_cloud_sdk_core import IAMTokenManager, ApiException
from pprint import pprint

import random
import string

configSecAdv={
    "authToken":None
}

SAConfiguration=None
Findings_API=None

def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def loadAndInit(confFile=None):
    # Credentials are read from a file
    with open(confFile) as confFile:
        configSecAdv.update(json.load(confFile))

    # Initialize the Watson Assistant client, use API V2
    if 'apikey' in configSecAdv:
        # Authentication via IAM
        authenticator=IAMAuthenticator(configSecAdv["apikey"])
        #configSecAdv["authToken"] = 'Bearer '+token_manager.request_token()['access_token']
    else:
        print('Expected apikey in credentials.')
        exit
    
    global SAConfiguration
    global Findings_API
    Findings_API=FindingsApiV1(authenticator=authenticator)
    Findings_API.set_service_url(configSecAdv["host"])

# Define parameters that we want to catch and some basic command help
def initParser(args=None):
    parser = argparse.ArgumentParser(description='Manage findings for IBM Cloud Security Advisor',
                                     prog='sec-adv-tool.py',
                                     usage='%(prog)s [-h | --interactive | --findings ] [options]')
    parser.add_argument("--interactive",dest='interactive', action='store_true', help='interactive mode')
    parser.add_argument("--findings",dest='findings', action='store_true', help='search findings')
    parser.add_argument("--config",dest='confFile', default='config.json', help='configuration file')

    return parser

def ListProviders():
    response=Findings_API.list_providers(configSecAdv["account_id"])
    pprint (response.result, indent=2)

def findingsByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput
    print("Searching findings by provider")
    response=Findings_API.list_occurrences(configSecAdv["account_id"],provider_id, page_size=page_size)
    pprint(response.result, indent=2)

def notesByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput
    print("Searching notes")
    response=Findings_API.list_notes(configSecAdv["account_id"], provider_id, page_size=page_size)
    pprint(response.result, indent=2)


def deleteNote():
    print("\nDELETE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    note_id = input("Please enter the note ID:\n")

    # Deletes the given `Note` from the system.
    response=Findings_API.delete_note(configSecAdv["account_id"], provider_id, note_id)
    pprint(response, indent=2)

def createNote():
    print("\nCREATE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with the note to create:\n")
    with open(fileInput) as noteFile:
        newNote=json.load(noteFile)
    newNote["provider_id"]=provider_id

    #response=Findings_API.create_note(configSecAdv["account_id"], provider_id, newNote)
    if newNote["kind"]=="CARD":
        response=Findings_API.create_note(configSecAdv["account_id"], provider_id,
                             new_short_description=newNote["short_description"],
                             new_long_description=newNote["long_description"],
                             new_kind=newNote["kind"],
                             new_id=newNote["id"],
                             new_reported_by=newNote["reported_by"],
                             new_card=newNote["card"])
    elif newNote["kind"]=="FINDING":
        response=Findings_API.create_note(configSecAdv["account_id"], provider_id,
                             new_short_description=newNote["short_description"],
                             new_long_description=newNote["long_description"],
                             new_kind=newNote["kind"],
                             new_id=newNote["id"],
                             new_reported_by=newNote["reported_by"],
                             new_finding=newNote["finding"])
    pprint(response, indent=2)

# def updateNote():
#     print("\nUPDATE A NOTE")
#     provider_id = input("Please enter the provider ID:\n")
#     note_id = input("Please enter the note ID:\n")
#     fileInput = input("Enter the filename with the note to update:\n")
#     with open(fileInput) as noteFile:
#         newNote=json.load(noteFile)
#     newNote["provider_id"]=provider_id

    
#     response=Findings_API.update_note(newNote, configSecAdv["authToken"], configSecAdv["account_id"], provider_id, note_id)
#         pprint(api_response, indent=2)
#     except ApiException as e:
#         print("Exception when calling APIs: %s\n" % e)

""" def insertOccurrence():
    print("\nCREATE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with findings occurrence to insert:\n")
    
    with open(fileInput) as occFile:
        newOcc=json.load(occFile)
    #if newOcc["provider_id"] != provider_id:
    #    print("Warning: Provider IDs do not match...")

    temp={"id":id_generator(), "note_name":configSecAdv["account_id"]+"/providers/" + provider_id + "/notes/"+"hl-test-finding"}
    newOcc.update(temp)
    pprint(newOcc, indent=2)

    print("Creating TEST occurrence")
    api_response = API_Occurrence_Instance.create_occurrence(newOcc, configSecAdv["authToken"], configSecAdv["account_id"], provider_id)
    pprint(api_response, indent=2)
    print("Created TEST occurrence")
 """
def deleteOccurrence():
    print("\nDELETE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    occurrence_id = input("Please enter the occurrence ID:\n")

    response=Findings_API.delete_occurrence(configSecAdv["account_id"],provider_id, occurrence_id)
    pprint(response.result, indent=2)

def queryGraph():
    qbody = input("Please enter the query body:\n")

    content_type="application/graphql"
    # query findings
    response=Findings_API.post_graph(configSecAdv["account_id"], qbody, content_type=content_type)
    pprint(response.result, indent=2)

def interactiveFindings():
    # Loop to get input
    while True:
        print("\n\n\nFINDINGS: (L)ist / (C)reate / (D)elete / (B)ack")
        # get some input
        minput = input("Please enter your input choice:\n")
        # if we catch a "bye" then exit
        if (minput == "B" or minput == "b"):
            break
        elif (minput == "L" or minput == "l"):
            findingsByProvider()
            pass
        # elif (minput == "C" or minput == "c"):
        #     insertOccurrence()
        #     pass
        # elif (minput == "D" or minput == "d"):
            deleteOccurrence()
            pass
        else:
            print("wrong option")
            pass

def interactiveNotes():
    # Loop to get input
    while True:
        print("\n\n\nNOTES: (L)ist / (C)reate / (U)pdate / (D)elete / (B)ack")
        # get some input
        minput = input("Please enter your input choice:\n")
        # if we catch a "bye" then exit
        if (minput == "B" or minput == "b"):
            break
        elif (minput == "L" or minput == "l"):
            notesByProvider()
            pass
        elif (minput == "C" or minput == "c"):
            createNote()
            pass
        # elif (minput == "U" or minput == "u"):
        #     updateNote()
        #     pass
        elif (minput == "D" or minput == "d"):
            deleteNote()
            pass
        else:
            print("wrong option")
            pass


def interactive():
    # Loop to get input
    while True:
        print("\n\n\n(F)indings / (P)roviders / (N)otes / (G)raph / e(X)it")
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
            interactiveNotes()
            pass
        elif (minput == "G" or minput == "g"):
            queryGraph()
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