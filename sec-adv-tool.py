# (C) 2020 IBM Corporation
#
# 
#


import json, requests, os
from os.path import join, dirname
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time
from ibm_cloud_sdk_core import IAMTokenManager, ApiException
from pprint import pprint
from dotenv import load_dotenv


import random
import string

Account_ID=None
Findings_API=None

def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def loadAndInit():
    load_dotenv()

    authenticator=IAMAuthenticator(os.getenv("SAT_APIKEY"))
    global Account_ID
    Account_ID=os.getenv("SAT_ACCOUNT_ID")

    global Findings_API
    Findings_API=FindingsApiV1(authenticator=authenticator)
    Findings_API.set_service_url(os.getenv("SAT_HOST"))


def ListProviders():
    response=Findings_API.list_providers(Account_ID)
    pprint (response.result, indent=2)

def findingsByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput
    print("Searching findings by provider")
    response=Findings_API.list_occurrences(Account_ID,provider_id, page_size=page_size)
    pprint(response.result, indent=2)

def notesByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput
    print("Searching notes")
    response=Findings_API.list_notes(Account_ID, provider_id, page_size=page_size)
    pprint(response.result, indent=2)
    while (response.result["next_page_token"] != ""):
            response=Findings_API.list_notes(Account_ID, provider_id, page_size=page_size, page_token=response.result["next_page_token"])
            pprint(response.result, indent=2)

def deleteNote():
    print("\nDELETE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    note_id = input("Please enter the note ID:\n")

    # Deletes the given `Note` from the system.
    response=Findings_API.delete_note(Account_ID, provider_id, note_id)
    pprint(response.result, indent=2)

def createNote():
    print("\nCREATE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with the note to create:\n")
    with open(fileInput) as noteFile:
        newNote=json.load(noteFile)
    newNote["provider_id"]=provider_id

    response=Findings_API.create_note(Account_ID, **newNote)

    pprint(response.result, indent=2)

def updateNote():
    print("\nUPDATE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    note_id = input("Please enter the note ID:\n")
    fileInput = input("Enter the filename with the note to update:\n")
    with open(fileInput) as noteFile:
        newNote=json.load(noteFile)
    newNote["provider_id"]=provider_id

    
    response=Findings_API.update_note(Account_ID,note_id=note_id, **newNote)
    pprint(response.result, indent=2)


def insertOccurrence():
    print("\nCREATE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with findings occurrence to insert:\n")
    
    with open(fileInput) as occFile:
        newOcc=json.load(occFile)
    newOcc["provider_id"]=provider_id
    
    temp_id=id_generator()
    temp_note_name=Account_ID+"/providers/" + provider_id + "/notes/"+newOcc["name"]
    pprint(newOcc, indent=2)

    print("Creating occurrence")
    response=Findings_API.create_occurrence(Account_ID, id=temp_id, note_name=temp_note_name, **newOcc)
    pprint(response.result, indent=2)

def deleteOccurrence():
    print("\nDELETE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    occurrence_id = input("Please enter the occurrence ID:\n")

    response=Findings_API.delete_occurrence(Account_ID,provider_id, occurrence_id)
    pprint(response.result, indent=2)

def queryGraph():
    qbody = input("Please enter the query body:\n")

    content_type="application/graphql"
    # query findings
    response=Findings_API.post_graph(Account_ID, qbody, content_type=content_type)
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
        elif (minput == "C" or minput == "c"):
            insertOccurrence()
            pass
        elif (minput == "D" or minput == "d"):
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
        elif (minput == "U" or minput == "u"):
            updateNote()
            pass
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
    loadAndInit()

    interactive()