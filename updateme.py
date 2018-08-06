#!/usr/bin/env python

########################################################################################################################
#										Simple update shortcut for this repository									   #
########################################################################################################################
#																		(C) Manuel Bernal Llinares <mbdebian@gmail.com>#
#																			Distributed under the Apache License 2.0   #
########################################################################################################################

# This script is design to run as a daemon, and periodically update this code

import os
import updateLogger as logger
import updateSettings
import subprocess


def main():
    config = updateSettings.getConfig()
    miLogger = logger.getLogger()

    miLogger.info("=" * 120)
    miLogger.info("Update session started, checking for updates...")
    command = "git pull >> " + config['logger']['ouputAndErrorFilePath'] + " 2>&1"
    miLogger.debug("Update command: " + command)
    p = subprocess.Popen(command, shell=True)
    if (p.wait()):
        miLogger.error("An error occurred while running the updates, please, check " + config['logger'][
            'ouputAndErrorFilePath'] + " for details.")
    else:
        miLogger.info("Check and update run with success!")

    miLogger.info("=" * 120)


if __name__ == "__main__":
    main()
