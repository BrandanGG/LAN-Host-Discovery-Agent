import requests
import os
import json

# Send data to API endpoint -- Data validation will be handled by the API / Engine server.
def upload_data(self, path:str):
        # Check if scans directory exists
        if not os.path.exists(path):
            print(f"Error: Directory '{path}' does not exist")
            return False
            
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return False
            
        # Get all files in the directory
        try:
            files = os.listdir(path)
        except OSError as e:
            print(f"Error reading directory '{path}': {e}")
            return False
            
        # Filter for JSON files
        json_files = [f for f in files if f.lower().endswith('.json')]
        
        if not json_files:
            print(f"No JSON files found in '{path}' directory")
            return False
            
        print(f"Found {len(json_files)} JSON files to upload")
        
        # Construct full API URL
        full_url = f"{self.api_url}{self.api_endpoint}"
        
        successful_uploads = 0
        failed_uploads = 0
        
        # Upload each JSON file
        for filename in json_files:
            file_path = os.path.join(path, filename)
            
            try:
                # Read JSON file
                with open(file_path, 'r') as f:
                    scan_data = json.load(f)
                
                # Prepare payload for API
                payload = {
                    "agent_id": self.agentName,
                    "data": scan_data,
                    "file_name": filename
                }
                
                # Send POST request
                response = requests.post(
                    full_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 201:
                    print(f"✓ Successfully uploaded {filename}")
                    successful_uploads += 1
                else:
                    print(f"✗ Failed to upload {filename}: HTTP {response.status_code}")
                    print(f"  Response: {response.text}")
                    failed_uploads += 1
                    
            except json.JSONDecodeError as e:
                print(f"✗ Error reading JSON file '{filename}': {e}")
                failed_uploads += 1
            except requests.exceptions.RequestException as e:
                print(f"✗ Network error uploading '{filename}': {e}")
                failed_uploads += 1
            except Exception as e:
                print(f"✗ Unexpected error uploading '{filename}': {e}")
                failed_uploads += 1
                
        # Summary
        print(f"\nUpload Summary:")
        print(f"  Successful: {successful_uploads}")
        print(f"  Failed: {failed_uploads}")
        print(f"  Total: {len(json_files)}")
        
        return successful_uploads > 0
        