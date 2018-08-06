# Makefile helper
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Environment
python_folder = python_install

all:
	@echo "<===|DEVOPS|===> [INFO] NO DEFAULT target set"

# Installation related targets
install: python_install install_requirements bin tmp logs
	@echo "<===|DEVOPS|===> [INSTALL] Platform"

python_install:
	@echo "<===|DEVOPS|===> [INSTALL] Preparing Python Virtual Environment"
	@pip install --upgrade --user virtualenv
	@virtualenv -p `which python3` $(python_folder)

install_requirements:
	@echo "<===|DEVOPS|===> [INSTALL] Installing platform requirements"
	@#python_install/bin/pip install pipreqs nose
	@$(python_folder)/bin/pip install -r requirements.txt

# Folders
tmp:
	@echo "<===|DEVOPS|===> [FOLDER] Creating temporary folders"
	@mkdir -p tmp
