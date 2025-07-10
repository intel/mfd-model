> [!IMPORTANT]  
> This project is under development. All source code and features on the main branch are for the purpose of testing or evaluation and not production ready.

# MFD Model
Module for handling Pydantic models used across multiple MFDs stored in subpackages.
The library utilizes the [project.optional-dependencies] section in pyproject.toml to specify optional dependencies for each subpackage

## Subpackages
Every subpackage can be installed separately by specifying the package name in square brackets after the main package name.
Structure:
```
├───<subpackage_name>
│   │   models.py
│   │   __init__.py
│   │   __version__.py
```

### config (used in pytest-mfd-config)
This subpackage contains models for configuration files. They are used in `pytest-mfd-config` to define configuration files and their structure.

### nvm
This subpackage contains models related with NVMs like `EETrack`, `Release`, ...\
They are used to handle upload / download / search of NVMs stored in NVMManager.

### artifacts_manager
This subpackage contains models for tested artifacts.

## Installation
To install 'config' models only use:
```bash
pip install mfd-model[config]
```

## How to add another subpackage? 
1. Create a new subpackage directory with the name of the subpackage.
2. Add `models.py` file with models definitions.
3. Add `__init__.py` file.
4. Add `__version__.py` file with version definition.
5. Update `pyproject.toml`:
   - add the requirements in [project.optional-dependencies] section, e.g.:
   ```
       data_processor = ["pydantic >= 2.0, < 3", "numpy >= 1.21.0"]  # Example dependencies
   ```

## OS supported:
* OS Independent

## Issue reporting

If you encounter any bugs or have suggestions for improvements, you're welcome to contribute directly or open an issue [here](https://github.com/intel/mfd-model/issues).