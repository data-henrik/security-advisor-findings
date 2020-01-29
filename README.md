# Work with Security Advisor findings
This is a small tool to interactively
- search for providers of notes and findings
- search for findings by a specific provider
- search for notes by a specific provider
- delete individual findings.
  
The tool is used to explore the Python SDK (https://github.com/ibm-cloud-security/security-advisor-findings-sdk-python) and to facilitate testing of custom findings.

1. Install the requirements.
2. Create a `config.json` to hold an API key and the account ID.
3. Launch `python3 sec-adv-findings.py -interactive`.