# Makefile helper
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Environment
python_folder = python_install

all:
	@echo "<===|DEVOPS|===> [INFO] NO DEFAULT target set"

# Installation related targets
install: python_install install_requirements bin tmp logs
	@echo "<===|DEVOPS|===> [INSTALL] Platform"
