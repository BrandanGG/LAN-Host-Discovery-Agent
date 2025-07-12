from agent import Agent
import asyncio
import json
import xmltodict
import os

async def scan_host(agent:Agent, ip:str):
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
            agent.up_hosts.append(ip)
        else:
            agent.down_hosts.append(ip)
            
        return result
    except Exception as e:
        print(f"Error scanning {ip}: {str(e)}")
        agent.down_hosts.append(ip)
        return str(e)
    
async def scan_alive(ip):
    try:
        process = await asyncio.create_subprocess_exec(
            "nmap",
            "-A",
            "-p-",
            "-T4",
            "-oX",
            "-",
            ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        xml_output = stdout.decode('utf-8')
        
        # Convert XML to JSON
        json_data = xmltodict.parse(xml_output)
        
        # Create scans directory if it doesn't exist
        os.makedirs('scans', exist_ok=True)
        
        # Save to file
        filename = f"scan_{ip.replace('.', '_')}.json"
        with open(f'scans/{filename}', 'w') as f:
            json.dump(json_data, f, indent=2)
            
        print(f"Scan results for {ip} saved to {filename}")
        return json_data
    except Exception as e:
        print(f"Error scanning {ip}: {str(e)}")
        return str(e)
    