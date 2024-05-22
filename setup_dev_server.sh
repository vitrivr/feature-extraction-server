#!/bin/bash

# Navigate to the src directory where the packages are located
cd src

# Loop through each sub-directory in src
for dir in */ ; do
    # Check if 'install_system_dependencies.sh' exists and is executable
    if [[ -x "${dir}install_system_dependencies.sh" ]]; then
        echo "Running system dependencies installation in ${dir}"
        # Run the install script
        ./${dir}install_system_dependencies.sh
    else
        echo "No install script in ${dir}, skipping..."
    fi
done

# Navigate back to the root directory
cd ..

# Execute Python script to extract development requirements
echo "Extracting development requirements..."
python extract_dev_requirements.py

# Install the required Python packages
echo "Installing development requirements..."
pip install -r dev_requirements.txt

echo "All setup tasks completed!"
