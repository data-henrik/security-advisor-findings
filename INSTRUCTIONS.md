# Instructions
Follow these instructions to set up and work with both the provided interactive tool as well as the code for IBM Cloud Functions.

## Tool to manage Security Advisor objects
A tool to work with objects of the IBM Cloud Security Advisor is located in the subdirectory [interactive-tool](/interactive-tool). You need to install necessary Python modules and configure environment variables in order to use it.

### Setup
The tool has been tested with Python 3.6. You need it to run the tool. Further setup requires only the following two steps.

1. Install the required modules by executing:   
    `pip install -r requirements.txt`
    Depending on your system, it could be that **pip3** is the command to use.
2. The necessary account details can be provided either through setting environment variables or setting them in a `.env` file. For the latter, copy over `.env.sample` to a new file `.env` and edit it to provide an IBM Cloud API key and your account ID. If you want to use environment variables, set them accordingly.

### Usage
Once the setup is done, you can start the tool. After executing `python3 sec-adv-tool.py`, a menu with options is printed. It offers:

1. List (P)roviders.
2. Work with (N)otes.
3. Work with (F)indings.
4. Perform a (G)raph query.
5. Or e(X)it the tool.

You can type your choice as upper- or lowercase character and then confirm with ENTER. Depending on the function, your are presented with a submenu.

### Deploy objects
To add custom findings to Security Advisor, you first need to define a new finding type. 
1. This is done in the (N)otes menu. 
2. There, choose to (C)reate a new note.
3. You are prompted for a provider ID. Enter **data_henrik** and hit ENTER.
4. Next, you are asked to provide the file with the note content to create. Enter `../samples/NOTE_externalUsers.json`. Thereafter, the tool should return the successful response with details on the created object.
5. Repeat steps 2), 3) and 4) twice and use the files `../samples/NOTE_inactiveUsers.json` and `../samples/NOTE_logdna.json` as input for step 4.

Some findings have additional Key Performance Indicators (KPIs) associated. They are used to not just flag an incident, but provide details on how many objects or events were found. Create them 
1. From the notes menu by using (c)reate again.
2. Enter **data_henrik** as provider.
3. Use `../samples/KPI_externalUsers.json` as file input.
4. Repeat the steps 1) to 3) and use `../samples/KPI_logdna.json` as file input for step 3).

To display findings in the Security Advisor dashboard, you need to define a card object.
1. Still in the notes menu, (c)reate a note again.
2. As done before, enter **data_henrik** as provider ID.
3. Now use `../samples/CARD_userCard.json` as file input.

### Optional: Verify objects
You can verify the successful deployment of objects from the previous section by using the tool again. In the tool,

1. Go to the (N)otes menu.
2. Choose (L)ist to query existing notes.
3. Enter **data_henrik** as provider ID. Next, the existing notes for the specified provider are printed.

## Cloud Functions
Cloud Functions are used to perform our own security scans and thereafter to create custom findings when necessary. To work with the Cloud Functions code, switch into the directory [functions](/functions).

### Deploy
To deploy the actions, follow these steps from within the [/functions](/functions) directory:

1. Create an IAM namespace:   
   `ibmcloud fn namespace create SecurityFindings`
2. Set the newly created namespace as default for the next commands.   
   `ibmcloud fn property set --namespace SecurityFindings`
3. Next, deploy the Cloud Functions package with its actions and sequences. The configuration for the objects is read from the file `manifest.yaml`.   
   `ibmcloud fn deploy`



### Access Management
The deployed actions need access privileges to scan the account configuration and to create, update and delete occurrences. Follow these steps to create the privileges:
1. In your browser, go to https://cloud.ibm.com/iam/groups
2. Click on **Create +** to create a new group.
3. Enter, e.g., **SecurityFindings** as **Name** and "Manage Cloud Functions access for security findings" as **Description**. Thereafter, click **Create**.
4. Next, click on **Service IDs** because we need to manage the service ID which was created for the IAM namespace (see **Cloud Functions**).
5. Click on **Add service ID +**. It allows you to select one or more service IDs. Find the ID **SecurityFindings** and select it. Then click on **Add to group +** (on the top right).
6. Now, click on the **Access policies** tab and then **Assign access**. 
7. For **IAM services** find **Security Advisor** in the dropdown list of services. Once selected, activate **Manager** for **Service access**. Then click **Add +** on the lower right. **Manager** is needed to delete occurrences.
8. For **Account management** find **User Management** and assign **Viewer** privilege. 
9. With the two assignments listed under **Access summary**, click on **Assign** to complete the process. The service ID for the Cloud Functions namespace has now the necessary privileges.

### LogDNA access
You need at least one instance of Activity Tracker with LogDNA deployed in order to take advantage of the event scanner. Go to https://cloud.ibm.com/observe/activitytracker for the setup.
1. Click on **View LogDNA** to launch the LogDNA dashboard.
2. Click on the cog icon on the left to go to the settings menu. There, click on **ORGANIZATION**.
3. Choose **API Keys**, then under **Service Keys** click to **Generate Service Key**.
4. Copy the new API key. It is needed to configure the Cloud Function action which scans LogDNA entries. The API key is used to access [the Export API which can be used for LogDNA queries](https://www.ibm.com/cloud/blog/search-logdna-records-from-the-command-line).

### Run actions manually
To run the actions manually, you should create a configuration file. 
1. In the **functions** directory, copy over `config.json.example` into a new file, e.g., `config.json`.
2. Edit the values for **account_id** and **provider_id**. You can obtain the account_id by running `ibmcloud account list`. Set **provider_id** to **data_henrik** because it is the value used in the sample objects created earlier.
3. The **email_domain** is used to scan for external users. If set to `ibm.com`, all users with email addresses not ending on that value would be flagged as external.
4. The value for **host** is one of the Security Advisor endpoints.

To run the action which searches LogDNA for specific events, you need to provide a special Activity Tracker configuration. An example is provided in the file `config.json.exampleAT`. 
- The JSON array **AT** has objects with the LogDNA API **key**
- and the related instance **region**.
- The value for **numHours** determines how many of the past hours to scan.
- The **query** holds the search term which will be used.
You can have multiple entries to search different instances or to perform several queries.

**Run the actions**

Assuming you have the configuration saved, you can run the actions similar to this:

`ibmcloud fn action invoke security_findings/inactiveUsersSeq -r -P config.json`

Instead of **inactiveUsersSeq** you can also run **externalUsersSeq** and **LogDNASeq**. Each action is actually a sequence of three individual actions: Obtain an IAM access token based on the provided API key, perform the scan, create or delete findings if necessary. The command above invokes the action and waits for the result (`-r`). The option `-P` is used to read the configuration parameters from the specified file. If no issue is found during the scan, you might see a result with a **404** message included. The reason is that the last action always tries to delete an existing finding if it is no longer needed.

You can see the created findings in
- the [IBM Cloud Security Advisor dashboard](https://cloud.ibm.com/security-advisor#/dashboard) or
- in the [Security Advisor Findings overview](https://cloud.ibm.com/security-advisor#/findings).

In case of problems you can check the [IBM Cloud Functions dashboard](https://cloud.ibm.com/functions/dashboard) for details of the invocation and error messages.

### Scheduled execution
It is possible to set up scheduled runs of the individual scans. You can utilize [IBM Cloud Functions triggers](https://cloud.ibm.com/docs/openwhisk?topic=cloud-functions-triggers) to schedule invocations. Details are left to the reader... :)
