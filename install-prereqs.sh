#!/bin/bash

## This script will install the necessary prerequisites for the project.
## It will install Python 3 and pip if they are not present as well as NMAP.
## supports Debian/Ubuntu based systems

# Check if the script is running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Function to check if a package is installed
check_package() {
    local package_name=$1
    if command -v "$package_name" &>/dev/null; then
        echo "$package_name is already installed"
        return 0
    else
        echo "$package_name is not installed"
        return 1
    fi
}

# Main script execution
echo "Checking prerequisites..."

# Check if NMAP is installed
if ! check_package "nmap"; then
    echo "NMAP is not installed. Installing..."
    sudo apt install -y nmap
fi

if ! check_package "python3"; then
    echo "Python 3 is not installed. Installing..."
    sudo apt install -y python3
    echo "Python 3 has been successfully installed!"
    else
        echo "Failed to install Python 3"
        exit 1
    fi
fi

if ! check_package "pip"; then
    echo "Pip is not installed. Installing..."
    sudo apt install -y pip
fi

sudo apt install -y python3-venv

echo "Python environment setup complete!"
