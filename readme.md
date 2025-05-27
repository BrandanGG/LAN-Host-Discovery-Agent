This application is indended to sit between each FW, physical / virtual.
These agents will have less impact to network traffic sitting in each segment rather than scanning through the firewall.

**Compatible with Debian / Ubuntu based systems**

**Not efficient enough to use on large networks, best suited for /22 or smaller networks. Efficiency can be increased by deploying multiple "Agents" or hosts, for example 2 agents in a /22 network can each scan a /23 network.**


To get started, run the install-prereqs.sh script.
Once pre-reqs are installed, run main.py with the arguments ip/cidr

This will be updated to load from a config.yml