#!/usr/bin/env python3
import toml
import os
from itertools import chain
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet, InvalidSpecifier

# Set the directory to search for pyproject.toml files
search_dirs = ["src"]

# Dictionary to hold dependencies per package
deps_dict = {}

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
                    # Process each dependency
                    for dep_str in pyproject_data['project']['dependencies']:
                        try:
                            req = Requirement(dep_str)
                            name = req.name.lower()
                            specifier = req.specifier
                            # If the package is already in the dict, combine specifiers
                            if name in deps_dict:
                                existing_specifier = deps_dict[name]
                                # Combine specifiers
                                combined_specifier = existing_specifier & specifier
                                # Check for conflicts
                                # A conflict exists if the combined specifier is not satisfied by any version
                                # Since we cannot test all versions, we'll check if the combined specifier is empty
                                # Only if both existing and new specifiers are non-empty and their intersection is empty, we have a conflict
                                if existing_specifier and specifier and not combined_specifier:
                                    print(f"ERROR: Conflicting versions for package '{name}':")
                                    print(f"  - {existing_specifier}")
                                    print(f"  - {specifier}")
                                    exit(1)
                                else:
                                    deps_dict[name] = combined_specifier
                            else:
                                deps_dict[name] = specifier
                        except InvalidSpecifier as e:
                            print(f"ERROR: Invalid specifier in dependency '{dep_str}': {e}")
                            exit(1)
                        except Exception as e:
                            print(f"ERROR: Failed to parse dependency '{dep_str}': {e}")
                            exit(1)

# Write the consolidated dependencies to dev_requirements.txt
with open('dev_requirements.txt', 'w') as req_file:
    for name in sorted(deps_dict.keys()):
        specifier = deps_dict[name]
        if specifier:
            req_file.write(f'{name}{specifier}\n')
        else:
            req_file.write(f'{name}\n')

print('Dependencies extracted to dev_requirements.txt')
