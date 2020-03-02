# Work with IBM Cloud Security Advisor objects

This is a small tool to interactively
- search for providers of notes and findings,
- search for notes by a specific provider,
- create a note (or card),
- delete an individual note,
- search for findings by a specific provider,
- create a new finding (occurrence),
- delete individual findings.
  
The tool is used to explore the Python SDK (https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python) and to facilitate testing of custom findings.

1. Install the requirements.
2. Create a `.env` to hold an API key, the account ID and host URI. Or use environment variables.
3. Launch `python3 sec-adv-findings.py`.

For more details follow the [instructions](/INSTRUCTIONS.md) on how to set up the entire project.


The following shows the beginning of an interactive session:   

![Command Line Tool](/screenshots/20200302_SecAdv_CLI1.png)