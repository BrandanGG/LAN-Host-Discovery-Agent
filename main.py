from agent import Agent
import asyncio
import yaml

def load_config(path:str):
     with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config

async def main(config:dict):
    # Create agent with config values
    network_config = config['network']
    ipcidr = f"{network_config['gateway']}/{network_config['cidr']}"
    agent = Agent(ipcidr)
    
    print(f"total number of hosts to be scanned: {agent.get_hosts()}")
    if agent.get_hosts() <= 254:
        octs = agent.gateway.split(".")
        ips = [f'{octs[0]}.{octs[1]}.{octs[2]}.{x}' for x in range(int(octs[3]), agent.get_hosts()+1)]
        tasks = [agent.scan_host(ip) for ip in ips]
        await asyncio.gather(*tasks)
        print(f'Total Number of Alive Hosts: {len(agent.up_hosts)}')
        for alive in agent.up_hosts:
            print(f'- {alive}')
    elif agent.get_hosts() <= 65534:
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
                
        tasks = [agent.scan_host(ip) for ip in ips]
        await asyncio.gather(*tasks)
        print(f'Total Number of Alive Hosts: {len(agent.up_hosts)}')
        for alive in agent.up_hosts:
            print(f'- {alive}')
    else:
        print("Network too large")
        return ValueError
    
if __name__ == "__main__":
    
    asyncio.run(main(load_config('config.yaml')))