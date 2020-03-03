# Cloud Functions for Security Scans

This subdirectory holds sample actions to populate findings (occurrences) in the IBM Cloud Security Advisor dashboard. See the [instructions](/INSTRUCTIONS.md) for steps on how to deploy the actions, grant access privileges and invoke the actions with the right configuration.

Each security scan is a sequence of three small actions:

1. The first action obtains an IAM access token (Identity and Access Management). It is needed to interface with the security advisor and for some scans.
2. The second action is different in each sequence. It connects to an IBM Cloud management API or to LogDNA to assess activity tracker / audit data.
3. The third action in the sequence creates individual occurrences for findings or KPI in the IBM Cloud Security Advisor.

![architecture diagram](/screenshots/SecAdv_Findings.png)