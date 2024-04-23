#!/usr/bin/env python3
import toml
import os
from itertools import chain

# Set the directory to search for pyproject.toml files
search_dirs = ["src"]

# List to hold all dependencies
all_deps = []

# Walk through the directory
for root, dirs, files in chain.from_iterable(os.walk(d) for d in search_dirs):
    for file in files:
        # Check for pyproject.toml file
        if file == 'pyproject.toml':
            file_path = os.path.join(root, file)
            print(f'Processing file: {file_path}')
            # Open and parse the TOML file
            with open(file_path, 'r') as toml_file:
                pyproject_data = toml.load(toml_file)
                # Check if the dependencies key is in the project section
                if 'project' in pyproject_data and 'dependencies' in pyproject_data['project']:
                    # Add dependencies to the list
                    all_deps.extend(pyproject_data['project']['dependencies'])

# Remove duplicates and sort
unique_deps = sorted(set(all_deps))

# Write the unique dependencies to requirements.txt
with open('dev_requirements.txt', 'w') as req_file:
    for dep in unique_deps:
        req_file.write(f'{dep}\n')

print('Dependencies extracted to dev_requirements.txt:')
