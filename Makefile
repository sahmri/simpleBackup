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
	@mkdir -p tmp/primesdbweb

bin:
	@echo "<===|DEVOPS|===> [FOLDER] Creating bin folder"
	@mkdir bin

logs:
	@echo "<===|DEVOPS|===> [FOLDER] Creating 'logs' folder"
	@mkdir logs
# END - Folders

update_requirements_file:
	@echo "<===|DEVOPS|===> [REQUIREMENTS] Updating requirements file"
	@#python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)
	@$(python_folder)/bin/pip freeze > requirements.txt

tests:
	@echo "<===|DEVOPS|===> [TESTS] Running unit tests"

# Housekeeping
clean_dev:
	@echo "<===|DEVOPS|===> [HOUSEKEEPING] Cleaning development environment"
	@rm -rf $(python_folder)

clean_tmp:
	@echo "<===|DEVOPS|===> [HOUSEKEEPING] Cleaning temporary folders"
	@rm -rf tmp

clean_bin:
	@echo "<===|DEVOPS|===> [HOUSEKEEPING] Cleaning external binaries"
	@rm -rf bin/*

clean: clean_tmp
	@echo "<===|DEVOPS|===> [HOUSEKEEPING] Cleaning"

clean_all: clean clean_dev
	@echo "<===|DEVOPS|===> [HOUSEKEEPING] Cleaning all environments"
# END - Housekeeping

.PHONY: install python_install install_requirements update_requirements_file tests clean_dev clean_all clean_tmp clean_bin clean
