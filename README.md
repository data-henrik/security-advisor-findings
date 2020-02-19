# Work with IBM Cloud Security Advisor

The [IBM Cloud Security Advisor](https://cloud.ibm.com/security-advisor) allows for centralized security management. It offers a unified dashboard that alerts security administrators for an IBM Cloud account of issues and helps them in resolving the issues. The advisor supports the integration of third-party vendors as well as custom findings. Using a REST API or programming language SDKs, it is possible to manage your own security metrics - from creating incident types and events to displaying them on the unified dashboard. 

# Overview

This repository has code
* for an [interactive tool](/interactive-tool) to work with Security Advisor objects,
* [sample](/sample) objects that can be created using the tool and be used by
* [Cloud Functions actions](/functions) which scan for custom security events and create related findings in the Security Advisor.

The [setup and usage instructions](/INSTRUCTIONS.md) are provided in a separate document.

# License

See the [License](/LICENSE) file.
