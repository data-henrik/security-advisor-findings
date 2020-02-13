# (C) 2020 IBM Corporation
#
# Use the Python SDK for the IBM Security Advisor Findings API to
# manage Providers, Notes and Occurrences.
#
# Doc: https://cloud.ibm.com/docs/services/security-advisor?topic=security-advisor-setup_custom
# API: https://cloud.ibm.com/apidocs/security-advisor/findings
# SDK: https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python


import json, os
from ibm_security_advisor_findings_api_sdk import FindingsApiV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pprint import pprint
from dotenv import load_dotenv

# For generating unique IDs
import random
import string

Account_ID=None
Findings_API=None

# Generate unique ID, needed for finding occurrences
def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# Set up environment by reading env variables and initialising SDK
def loadAndInit():
    # load .env if available
    load_dotenv()

    # Account ID is needed for most API functions
    global Account_ID
    Account_ID=os.getenv("SAT_ACCOUNT_ID")
    # SDK instance
    global Findings_API

    # initialize IAM authentication based on API key
    authenticator=IAMAuthenticator(os.getenv("SAT_APIKEY"))
    # initialize API / SDK
    Findings_API=FindingsApiV1(authenticator=authenticator)
    Findings_API.set_service_url(os.getenv("SAT_HOST"))

# Obtain the list of available (visible) providers
def ListProviders():
    print("\nListing providers")
    response=Findings_API.list_providers(Account_ID)
    pprint (response.result, indent=2)
    # if there is more data, fetch and print it
    while (response.result["next_page_token"] != None):
            response=Findings_API.list_providers(Account_ID, page_token=response.result["next_page_token"])
            pprint(response.result, indent=2)

# Obtain the list of all findings / occurrences
# A provider ID needs to be typed in on the command line.
def findingsByProvider():
    provinput = input("Please enter the provider ID:\n")
    page_size=50
    provider_id=provinput
    print("Searching findings by provider")
    response=Findings_API.list_occurrences(Account_ID,provider_id, page_size=page_size)
    pprint(response.result, indent=2)
    # if there is more data, fetch and print it
    while (response.result["next_page_token"] != ""):
            response=Findings_API.list_occurrences(Account_ID, provider_id, page_size=page_size, page_token=response.result["next_page_token"])
            pprint(response.result, indent=2)

# Obtain the list of all notes (card, kpi, finding)
# A provider ID needs to be typed in on the command line.
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

# Delete a note identified by provider and its ID
def deleteNote():
    print("\nDELETE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    note_id = input("Please enter the note ID:\n")

    # Deletes the given `Note` from the system.
    response=Findings_API.delete_note(Account_ID, provider_id, note_id)
    pprint(response.result, indent=2)

# Create a note (card, kpi, finding)
def createNote():
    print("\nCREATE A NOTE")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with the note to create:\n")
    # Load the file
    with open(fileInput) as noteFile:
        newNote=json.load(noteFile)
    
    # Set the correct provider_id
    newNote["provider_id"]=provider_id
    # Create the note based on file content
    response=Findings_API.create_note(Account_ID, **newNote)
    pprint(response.result, indent=2)

# Update an existing note, similar to creating it
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

# Create / insert a new finding occurrence
def insertOccurrence():
    print("\nCREATE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    fileInput = input("Enter the filename with findings occurrence to insert:\n")
    
    with open(fileInput) as occFile:
        newOcc=json.load(occFile)
    newOcc["provider_id"]=provider_id
    # Generate the occurrence ID
    temp_id=id_generator()
    # Compose the note name based on account, provider and note ID
    temp_note_name=Account_ID+"/providers/" + provider_id + "/notes/"+newOcc["name"]
    
    print("Creating occurrence")
    response=Findings_API.create_occurrence(Account_ID, id=temp_id, note_name=temp_note_name, **newOcc)
    pprint(response.result, indent=2)

# Delete an existing occurrence
def deleteOccurrence():
    print("\nDELETE A FINDING")
    provider_id = input("Please enter the provider ID:\n")
    occurrence_id = input("Please enter the occurrence ID:\n")

    response=Findings_API.delete_occurrence(Account_ID,provider_id, occurrence_id)
    pprint(response.result, indent=2)

# Can be used for more advanced queries
def queryGraph():
    qbody = input("Please enter the query body:\n")

    content_type="application/graphql"
    # query findings
    response=Findings_API.post_graph(Account_ID, qbody, content_type=content_type)
    pprint(response.result, indent=2)

# Handle input to decide on action for Findings submenu
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

# Handle input to decide on action for Notes submenu
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


# Handle input in "main" menu
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
# Main program, for now just load the environment and display our basic options menu
#
if __name__ == '__main__':
    loadAndInit()

    interactive()