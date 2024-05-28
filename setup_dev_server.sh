#!/bin/bash

# Loop through each sub-directory in src
for dir in src/* ; do
    # Check if 'install_system_dependencies.sh' exists
    if [[ -f "${dir}/install_system_dependencies.sh" ]]; then
        # Ensure the script is executable
        chmod +x "${dir}/install_system_dependencies.sh"
        echo "Running system dependencies installation in ${dir}"
        # Run the install script
        ./${dir}/install_system_dependencies.sh
    else
        echo "No install script in ${dir}, skipping..."
    fi
done

# Execute Python script to extract development requirements
echo "Extracting development requirements..."
python extract_dev_requirements.py

# Install the required Python packages
echo "Installing development requirements..."
pip install -r dev_requirements.txt

echo "All setup tasks completed!"
