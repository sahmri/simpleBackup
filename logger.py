#!/usr/bin/env python

########################################################################################################################
#													Simple Logging System											   #
########################################################################################################################
#																		(C) Manuel Bernal Llinares <mbdebian@gmail.com>#
#																			Distributed under the Apache License 2.0   #
########################################################################################################################

import os
import logging
import settings  # Get the settings singleton that should have already been initialized

_logger = None


def getLogger():
    global _logger
    if not _logger:
        # print("Preparing logger")
        # Instantiate the _logger
        config = settings.getConfig()

        # Create the logger
        _logger = logging.getLogger(config["logger"]["namespace"])

        # Set formatter
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(name)s --- %(message)s')

        # Set logger handler
        handler = logging.FileHandler(config["logger"]["filePath"])
        handler.setFormatter(formatter)
        # Set logging level
        if "level" in config["logger"]:
            if "debug" in config["logger"]["level"]:
                handler.setLevel(logging.DEBUG)
            elif "critical" in config["logger"]["level"]:
                handler.setLevel(logging.CRITICAL)
            elif "error" in config["logger"]["level"]:
                handler.setLevel(logging.ERROR)
            elif "fatal" in config["logger"]["level"]:
                handler.setLevel(logging.FATAL)
            elif "warning" in config["logger"]["level"]:
                handler.setLevel(logging.WARNING)
            else:
                handler.setLevel(logging.INFO)
        else:
            handler.setLevel(logging.INFO)
        _logger.setLevel(handler.level)

        # Add handler to logger
        _logger.addHandler(handler)
    return _logger  # logging.getLogger(settings.getConfig()["logger"]["namespace"])


def main():
    print("This module is not designed to play alone. Sorry.")


if __name__ == "__main__":
    main()
