from agent import Agent
from scan import scan_host, scan_alive
import asyncio
import yaml
import socket


def load_config(path:str):
     with open(path, 'r') as file:
        config = yaml.safe_load(file)
        network_config = config['network']
        ipcidr = f"{network_config['gateway']}/{network_config['cidr']}"
        agent_config = config['agent']
        hostname = f"{agent_config['agent-hostname']}"
        if f"{agent_config['agent-hostname']}" == "":
            hostname = socket.gethostname()
        agent = Agent(ipcidr, hostname)
        return agent
    
async def main(agent:Agent):
    ## Initial Probe for online or not
    print(f"Agent {agent.agentName} is starting\ntotal number of hosts to be scanned: {agent.get_hosts()}")
    if agent.get_hosts() <= 254: #/24 or smaller
        octs = agent.gateway.split(".")
        ips = [f'{octs[0]}.{octs[1]}.{octs[2]}.{x}' for x in range(int(octs[3]), agent.get_hosts()+1)]
        tasks = [scan_host(agent, ip) for ip in ips]
        await asyncio.gather(*tasks)
        print(f'Total Number of Alive Hosts: {len(agent.up_hosts)}')
        for alive in agent.up_hosts:
            print(f'- {alive}')
    elif agent.get_hosts() <= 65534: #/16 - /24
        octs = agent.gateway.split(".")
        start_third_octet = int(octs[2])
        start_fourth_octet = int(octs[3])
        
        remaining_hosts = agent.get_hosts()
        
        ips = []
        current_third = start_third_octet
        current_fourth = start_fourth_octet
        
        while remaining_hosts > 0:
            ips_in_current_third = min(256 - current_fourth, remaining_hosts)
            
            for fourth in range(current_fourth, current_fourth + ips_in_current_third):
                ips.append(f'{octs[0]}.{octs[1]}.{current_third}.{fourth}')
            
            remaining_hosts -= ips_in_current_third
            
            if remaining_hosts > 0:
                current_third += 1
                current_fourth = 0
                
        tasks = [scan_host(agent,ip) for ip in ips]
        await asyncio.gather(*tasks)
        print(f'Total Number of Alive Hosts: {len(agent.up_hosts)}')
        for alive in agent.up_hosts:
            print(f'- {alive}')
    else:
        print("Network too large")
        return ValueError

    #Follow up probe on active devices
    print("\nStarting detailed scans of active hosts...")
    tasks = [scan_alive(ip) for ip in agent.up_hosts]
    results = await asyncio.gather(*tasks)
    
    # Process results if needed
    for ip, result in zip(agent.up_hosts, results):
        if isinstance(result, dict):  # Check if result is JSON data
            print(f"Successfully scanned {ip}")
        else:
            print(f"Failed to scan {ip}: {result}")

if __name__ == "__main__": 
    agent = load_config('config.yaml')
    asyncio.run(main(agent))
    #asyncio.run(activeHosts())