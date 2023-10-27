#!/bin/bash

# Directory containing plugins
plugins_directory=${PLUGINS_DIR:-/plugins}

# Iterate over each directory inside plugins_directory
for plugin in "$plugins_directory"/*; do
    if [ -d "$plugin" ] && [ -e "$plugin/pyproject.toml" ]; then
        cd "$plugin"
        
        # If install_system_dependencies.sh exists, execute it
        if [ -e "install_system_dependencies.sh" ]; then
            echo "Installing system dependencies for $plugin..."
            chmod +x "install_system_dependencies.sh"
            "./install_system_dependencies.sh"
        fi
        
        # Use flit to install the plugin
        flit install
        cd - # Return to the previous directory

        echo "Installed $plugin"
        echo "_________________________"
    fi
done

cd /app/feature_extraction_server-core

if [ -e "install_system_dependencies.sh" ]; then
    echo "Installing system dependencies for core..."
    chmod +x "install_system_dependencies.sh"
    apt-get upgrade && apt-get update
    "./install_system_dependencies.sh"
fi

flit install

cd ..

# # IDLE
# echo "Entering idle mode..."
# while true; do
#     sleep 1
# done

gunicorn -w ${WORKERS} -b :5000 --timeout 600 --preload 'feature_extraction_server.flask.entrypoint:entrypoint()'
