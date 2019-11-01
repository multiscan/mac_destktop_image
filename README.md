# mac_destktop_image
More flexible desktop image cycler

## Installation
 * Clone the repo where you want
 * make sure you have the following packages installed and usable by python:
    - ruamel.yaml
    - sqlite3
 * copy `desktop_image.yml.example` as `desktop_image.yml` and edit with your preferences

### With pyenv
My method of choice of python scripts is using [pyenv](https://github.com/pyenv/pyenv). This script was tested with version 3.5.4 but it might work with other versions. Add a `.python-version` file in your installation directory and, provided the required packages are installed in that version, the script should work.

## Usage
The command is the script `dimg`. 

### Single shot
By default, the script changes your desktop image. The image is chosen randomly from the directories listed in your configuration file. J
