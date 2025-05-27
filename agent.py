import asyncio
import math
class Agent:
    def __init__(self, ipcidr:str):
        self.gateway = ipcidr.split("/")[0]
        self.cidr = int(ipcidr.split("/")[1])
        self.up_hosts = []
        self.down_hosts = []

    def get_hosts(self):
        bits = 32 - self.cidr
        return int((math.pow(2, bits)-2))
        
    async def scan_host(self, ip):
        try:
            process = await asyncio.create_subprocess_exec(
                "nmap",
                "-sn",
                ip,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            result = stdout.decode('utf-8')
            print(f"Scan result for {ip}: {result}")
            
            # Process the result
            if "Host is up" in result:
                self.up_hosts.append(ip)
            else:
                self.down_hosts.append(ip)
                
            return result
        except Exception as e:
            print(f"Error scanning {ip}: {str(e)}")
            self.down_hosts.append(ip)
            return str(e)
        
    def print_scan_summary(self):
        print(f"\nHosts that are up ({len(self.up_hosts)}):")
        for host in self.up_hosts:
            print(f"- {host}")
            
        print(f"\nHosts that are down ({len(self.down_hosts)}):")
        for host in self.down_hosts:
            print(f"- {host}")
            
    async def run(self):
        print(f"Starting network scan for {self.gateway}/{self.subnetmask}")
        
