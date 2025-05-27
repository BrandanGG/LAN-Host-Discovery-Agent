import asyncio
import math
class Agent:
    def __init__(self, ipcidr:str, agentName:str):
        self.gateway = ipcidr.split("/")[0]
        self.cidr = int(ipcidr.split("/")[1])
        self.agentName = agentName
        self.up_hosts = []
        self.down_hosts = []

    def get_hosts(self):
        bits = 32 - self.cidr
        return int((math.pow(2, bits)-2))
        
    def print_scan_summary(self):
        print(f"\nHosts that are up ({len(self.up_hosts)}):")
        for host in self.up_hosts:
            print(f"- {host}")
            
        print(f"\nHosts that are down ({len(self.down_hosts)}):")
        for host in self.down_hosts:
            print(f"- {host}")
            
    async def run(self):
        print(f"Starting network scan for {self.gateway}/{self.subnetmask}")
        
